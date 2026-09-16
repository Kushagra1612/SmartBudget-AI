import re
import logging

from app.utils.transaction_cleaner import TransactionCleaner
from app.categorizer.category_engine import CategoryEngine


logger = logging.getLogger(__name__)


class TextTransactionParser:

    DATE_PATTERN = re.compile(
        r"\b(\d{2}/\d{2}/\d{2,4})\b"
    )

    AMOUNT_PATTERN = re.compile(
        r"\b\d{1,3}(?:,\d{3})*(?:\.\d{2})\b"
    )

    # Same footer/boilerplate keyword list as UniversalStatementParser
    # (matched against a punctuation/whitespace-stripped copy of each
    # line, for the same reason: PDF text extraction often squashes
    # these phrases together with no spaces at all). Without this,
    # trailing statement summaries and legal notices get appended to
    # whatever transaction is currently being built -- most severely
    # the LAST one in the statement, which has no following date to
    # stop it.
    FOOTER_KEYWORDS = (
        "statementsummary",
        "drcountcrcount",
        "registeredoffice",
        "gstin",
        "gstn",
        "closingbalanceincludes",
        "contentsofthisstatement",
        "computergeneratedstatement",
        "doesnotrequiresignature",
        "generatedon",
        "generatedby",
        "requestingbranchcode",
        "endofstatement",
    )

    @classmethod
    def is_footer_line(cls, line: str) -> bool:

        squashed = re.sub(
            r"[^a-z0-9]",
            "",
            line.lower(),
        )

        return any(
            keyword in squashed
            for keyword in cls.FOOTER_KEYWORDS
        )

    @staticmethod
    def parse(text: str):

        if not text:
            return []

        raw_transactions = (
            TextTransactionParser
            .extract_raw_transactions(text)
        )

        typed_transactions = (
            TextTransactionParser
            .infer_transaction_types(raw_transactions)
        )

        deduped_transactions = (
            TextTransactionParser
            .remove_duplicates(typed_transactions)
        )

        categorized_transactions = [
            CategoryEngine.categorize(transaction)
            for transaction in deduped_transactions
        ]

        logger.info(
            "Universal text parser extracted %d transactions",
            len(categorized_transactions),
        )

        return categorized_transactions

    @classmethod
    def extract_raw_transactions(cls, text: str):
        """
        First pass: split the text into per-transaction blocks and
        pull out date/description/amount/balance, WITHOUT yet
        deciding debit vs credit -- that needs a second pass once we
        have every transaction's balance in order (see
        infer_transaction_types).
        """

        lines = text.splitlines()

        current_transaction = None

        raw_transactions = []

        in_footer = False

        for line in lines:

            line = " ".join(line.split())

            if not line:
                continue

            dates = cls.DATE_PATTERN.findall(line)

            if dates:

                # A genuine transaction always resumes normal
                # processing, even if we were mid-footer.
                in_footer = False

                if current_transaction:

                    parsed = cls.build_raw_transaction(
                        current_transaction
                    )

                    if parsed:
                        raw_transactions.append(parsed)

                current_transaction = {
                    "lines": [line],
                }

                continue

            if in_footer:

                # Already inside a footer/boilerplate section --
                # skip every line unconditionally until the next
                # real transaction starts (handles footers spanning
                # multiple physical PDF lines).
                continue

            if cls.is_footer_line(line):

                in_footer = True
                continue

            if current_transaction:

                # Transaction descriptions can wrap onto multiple
                # lines.
                current_transaction["lines"].append(line)

        if current_transaction:

            parsed = cls.build_raw_transaction(
                current_transaction
            )

            if parsed:
                raw_transactions.append(parsed)

        return raw_transactions

    @classmethod
    def build_raw_transaction(cls, data):

        text = " ".join(data["lines"])

        dates = cls.DATE_PATTERN.findall(text)

        amounts = cls.AMOUNT_PATTERN.findall(text)

        if not dates:
            return None

        transaction_date = TransactionCleaner.clean_date(
            dates[0]
        )

        if transaction_date is None:
            return None

        numeric_amounts = []

        for amount in amounts:

            try:
                value = float(amount.replace(",", ""))
                numeric_amounts.append(value)

            except ValueError:
                continue

        if not numeric_amounts:
            return None

        # Usually the final amount is the balance.
        balance = numeric_amounts[-1]

        # Second-last amount is generally the transaction amount.
        transaction_amount = (
            numeric_amounts[-2]
            if len(numeric_amounts) >= 2
            else 0.0
        )

        if transaction_amount <= 0:
            return None

        description = text

        for date_value in dates:
            description = description.replace(date_value, "")

        for amount in amounts:
            description = description.replace(amount, "")

        description = " ".join(description.split())

        if not description:
            return None

        return {
            "date": transaction_date,
            "description": TransactionCleaner.clean_description(
                description
            ),
            "amount": transaction_amount,
            "balance": balance,
        }

    @classmethod
    def infer_transaction_types(cls, transactions: list[dict]):
        """
        Second pass: decide debit vs credit for each transaction by
        comparing it to the PREVIOUS transaction's balance (the one
        that came right before it in time) -- this parser's output is
        chronological ascending, same as UniversalStatementParser, so
        the same comparison logic applies.

        The previous version of this file hardcoded every transaction
        as a debit and never produced a credit/income transaction at
        all, regardless of what the statement actually showed.
        """

        if not transactions:
            return []

        parsed_transactions = []

        previous_balance = None

        for transaction in transactions:

            amount = transaction["amount"]
            current_balance = transaction["balance"]

            debit = 0.0
            credit = 0.0

            if previous_balance is None:

                # First transaction -- no earlier balance to compare
                # against. Fall back to debit as a safe default.
                debit = amount

            else:

                difference = current_balance - previous_balance

                if difference > 0:
                    credit = amount
                elif difference < 0:
                    debit = amount
                else:
                    debit = amount

            parsed_transactions.append(
                {
                    "date": transaction["date"],
                    "description": transaction["description"],
                    "debit": debit,
                    "credit": credit,
                    "balance": current_balance,
                }
            )

            previous_balance = current_balance

        return parsed_transactions

    @staticmethod
    def remove_duplicates(transactions: list[dict]):

        unique_transactions = []

        seen = set()

        for transaction in transactions:

            identifier = (
                transaction["date"],
                transaction["description"],
                transaction["debit"],
                transaction["credit"],
                transaction["balance"],
            )

            if identifier not in seen:

                seen.add(identifier)
                unique_transactions.append(transaction)

        return unique_transactions