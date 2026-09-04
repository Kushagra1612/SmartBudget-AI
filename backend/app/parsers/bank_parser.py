import camelot
import pdfplumber

from app.parsers.header_detector import HeaderDetector
from app.parsers.bank_identifier import BankIdentifier

from app.utils.parser_helpers import ParserHelper
from app.utils.transaction_cleaner import TransactionCleaner

from app.categorizer.category_engine import CategoryEngine


class BankStatementParser:

    @staticmethod
    def extract_tables(pdf_path: str):
        """
        Extract tables using Camelot and return categorized transactions.

        Tries "lattice" first (most accurate when it works, but only
        detects tables with visible ruled borders around each cell,
        which not every bank statement has), then falls back to
        "stream" (finds columns by text alignment instead -- catches
        statements with no drawn grid lines). Confirmed directly: a
        borderless test table that lattice found zero rows in was
        correctly picked up by stream.
        """

        for flavor in ("lattice", "stream"):

            try:

                tables = camelot.read_pdf(
                    pdf_path,
                    pages="all",
                    flavor=flavor,
                )

                if tables.n == 0:
                    continue

                cleaned_transactions = []

                for table in tables:

                    df = table.df

                    if df.empty:
                        continue

                    # Detect header
                    df = HeaderDetector.detect(df)

                    # Normalize columns
                    df = ParserHelper.normalize_columns(df)

                    # Remove duplicate columns
                    df = df.loc[:, ~df.columns.duplicated()]

                    records = df.to_dict(orient="records")

                    for row in records:

                        transaction = {

                            "date": TransactionCleaner.clean_date(
                                row.get("date", "")
                            ),

                            "description": TransactionCleaner.clean_description(
                                row.get("description", "")
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

                        # Skip invalid date
                        if transaction["date"] is None:
                            continue

                        # Skip rows without description and amount
                        if (
                            transaction["description"] == ""
                            and transaction["debit"] == 0
                            and transaction["credit"] == 0
                        ):
                            continue

                        transaction = CategoryEngine.categorize(
                            transaction
                        )

                        cleaned_transactions.append(transaction)

                if cleaned_transactions:

                    return {
                        "method": f"camelot-{flavor}",
                        "transactions": cleaned_transactions,
                    }

            except Exception as e:

                print(f"Camelot ({flavor}) parsing failed:", e)

        return None

    @staticmethod
    def extract_text(pdf_path: str):

        text = ""

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

        return text

    @classmethod
    def parse(cls, pdf_path: str):

        result = cls.extract_tables(pdf_path)

        if result is not None:
            return result

        # Neither table-extraction flavor found anything usable. There's
        # no text-based transaction parser here (yet) to fall back to --
        # grabbing the text and guessed bank is purely for the log line
        # below, so a failed upload leaves a trace of which bank it was
        # and roughly how much text was in it, useful for figuring out
        # which statement layouts still need support.
        text = cls.extract_text(pdf_path)
        bank = BankIdentifier.identify(text)

        print(
            f"No transactions extracted from PDF "
            f"(bank guessed: {bank}, {len(text)} chars of text found)"
        )

        return None