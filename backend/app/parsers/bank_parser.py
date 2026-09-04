import logging

import camelot
import pdfplumber

from app.parsers.header_detector import HeaderDetector
from app.parsers.bank_identifier import BankIdentifier
from app.utils.parser_helpers import ParserHelper
from app.utils.transaction_cleaner import TransactionCleaner
from app.categorizer.category_engine import CategoryEngine


logger = logging.getLogger(__name__)


class BankStatementParser:

    @staticmethod
    def extract_tables(pdf_path: str):
        """
        Extract tables using Camelot and return categorized transactions.

        First tries Camelot's lattice flavor for tables with visible
        borders. If that does not produce usable transactions, it tries
        the stream flavor for borderless tables.
        """

        for flavor in ("lattice", "stream"):

            try:
                logger.info(
                    "Trying Camelot '%s' parser for file: %s",
                    flavor,
                    pdf_path,
                )

                tables = camelot.read_pdf(
                    pdf_path,
                    pages="all",
                    flavor=flavor,
                )

                logger.info(
                    "Camelot '%s' found %d tables",
                    flavor,
                    tables.n,
                )

                if tables.n == 0:
                    continue

                cleaned_transactions = []

                for table_index, table in enumerate(tables):

                    logger.info(
                        "Processing table %d using '%s'",
                        table_index + 1,
                        flavor,
                    )

                    df = table.df

                    if df.empty:
                        logger.info(
                            "Table %d is empty",
                            table_index + 1,
                        )
                        continue

                    logger.info(
                        "Table %d has %d rows and %d columns",
                        table_index + 1,
                        len(df),
                        len(df.columns),
                    )

                    # Detect header
                    df = HeaderDetector.detect(df)

                    # Normalize column names
                    df = ParserHelper.normalize_columns(df)

                    # Remove duplicate columns
                    df = df.loc[:, ~df.columns.duplicated()]

                    records = df.to_dict(
                        orient="records"
                    )

                    for row in records:

                        transaction = {
                            "date": TransactionCleaner.clean_date(
                                row.get("date", "")
                            ),
                            "description": (
                                TransactionCleaner.clean_description(
                                    row.get("description", "")
                                )
                            ),
                            "debit": TransactionCleaner.clean_amount(
                                row.get("debit", "")
                            ),
                            "credit": TransactionCleaner.clean_amount(
                                row.get("credit", "")
                            ),
                            "balance": TransactionCleaner.clean_amount(
                                row.get("balance", "")
                            ),
                        }

                        # Skip rows with invalid dates
                        if transaction["date"] is None:
                            continue

                        # Skip completely empty transaction rows
                        if (
                            transaction["description"] == ""
                            and transaction["debit"] == 0
                            and transaction["credit"] == 0
                        ):
                            continue

                        # Categorize transaction
                        transaction = CategoryEngine.categorize(
                            transaction
                        )

                        cleaned_transactions.append(
                            transaction
                        )

                logger.info(
                    "Camelot '%s' extracted %d valid transactions",
                    flavor,
                    len(cleaned_transactions),
                )

                if cleaned_transactions:
                    return {
                        "method": f"camelot-{flavor}",
                        "transactions": cleaned_transactions,
                    }

            except Exception:
                logger.exception(
                    "Camelot '%s' parsing failed for file: %s",
                    flavor,
                    pdf_path,
                )

        logger.warning(
            "No transactions could be extracted using Camelot"
        )

        return None

    @staticmethod
    def extract_text(pdf_path: str):
        """
        Extract all available text from the PDF using pdfplumber.
        """

        text = ""

        try:
            with pdfplumber.open(pdf_path) as pdf:

                logger.info(
                    "PDF contains %d pages",
                    len(pdf.pages),
                )

                for page_number, page in enumerate(
                    pdf.pages,
                    start=1,
                ):

                    extracted = page.extract_text()

                    if extracted:
                        text += extracted + "\n"

                        logger.info(
                            "Extracted %d characters from page %d",
                            len(extracted),
                            page_number,
                        )
                    else:
                        logger.warning(
                            "No text extracted from page %d",
                            page_number,
                        )

        except Exception:
            logger.exception(
                "Failed to extract text from PDF: %s",
                pdf_path,
            )

        return text

    @classmethod
    def parse(cls, pdf_path: str):
        """
        Parse a bank statement.

        First attempts table extraction with Camelot. If no transactions
        are found, extracts PDF text for debugging and bank identification.
        """

        logger.info(
            "Starting bank statement parsing: %s",
            pdf_path,
        )

        # Try table extraction
        result = cls.extract_tables(pdf_path)

        if result is not None:
            logger.info(
                "Successfully parsed %d transactions using %s",
                len(result["transactions"]),
                result["method"],
            )

            return result

        # Fallback: Extract text
        logger.info(
            "Camelot could not extract transactions. "
            "Trying PDF text extraction."
        )

        # IMPORTANT: Define text first
        text = cls.extract_text(pdf_path)

        # Then use text
        logger.info(
            "PDF TEXT PREVIEW:\n%s",
            text[:3000],
        )

        bank = BankIdentifier.identify(text)

        logger.warning(
            "No transactions extracted from PDF. "
            "Bank guessed: %s | Extracted text length: %d characters",
            bank,
            len(text),
        )

        return None