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
        """

        try:
            tables = camelot.read_pdf(
                pdf_path,
                pages="all",
                flavor="lattice",
            )

            if tables.n == 0:
                return None

            cleaned_transactions = []

            for table in tables:

                df = table.df

                if df.empty:
                    continue

                # Detect header row
                df = HeaderDetector.detect(df)

                # Normalize column names
                df = ParserHelper.normalize_columns(df)

                # Convert to list of dictionaries
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

                    # Skip blank rows
                    if (
                        transaction["date"] == ""
                        and transaction["description"] == ""
                        and transaction["debit"] == 0
                        and transaction["credit"] == 0
                        and transaction["balance"] == 0
                    ):
                        continue

                    # NEW: Categorize transaction
                    transaction = CategoryEngine.categorize(transaction)

                    cleaned_transactions.append(transaction)

            if cleaned_transactions:

                return {
                    "method": "camelot",
                    "transactions": cleaned_transactions,
                }

        except Exception as e:
            print(f"Camelot parsing failed: {e}")

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

        text = cls.extract_text(pdf_path)

        bank = BankIdentifier.identify(text)

        return {
            "method": "pdfplumber",
            "bank": bank,
            "raw_text": text,
        }