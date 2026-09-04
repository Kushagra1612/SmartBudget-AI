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

    @staticmethod
    def parse(text: str):

        if not text:
            return []

        lines = text.splitlines()

        transactions = []

        current_transaction = None

        for line in lines:

            line = " ".join(line.split())

            if not line:
                continue

            dates = TextTransactionParser.DATE_PATTERN.findall(
                line
            )

            amounts = TextTransactionParser.AMOUNT_PATTERN.findall(
                line
            )

            # A potential transaction generally starts with a date
            if dates:

                # Save previous transaction
                if current_transaction:

                    parsed = (
                        TextTransactionParser
                        .build_transaction(
                            current_transaction
                        )
                    )

                    if parsed:
                        transactions.append(parsed)

                current_transaction = {
                    "lines": [line],
                }

            elif current_transaction:

                # Transaction descriptions can wrap onto multiple lines
                current_transaction["lines"].append(
                    line
                )

        # Save final transaction
        if current_transaction:

            parsed = (
                TextTransactionParser
                .build_transaction(
                    current_transaction
                )
            )

            if parsed:
                transactions.append(parsed)

        logger.info(
            "Universal text parser extracted %d transactions",
            len(transactions),
        )

        return transactions

    @staticmethod
    def build_transaction(data):

        text = " ".join(
            data["lines"]
        )

        dates = (
            TextTransactionParser
            .DATE_PATTERN
            .findall(text)
        )

        amounts = (
            TextTransactionParser
            .AMOUNT_PATTERN
            .findall(text)
        )

        if not dates:
            return None

        # Parse date
        transaction_date = (
            TransactionCleaner.clean_date(
                dates[0]
            )
        )

        if transaction_date is None:
            return None

        numeric_amounts = []

        for amount in amounts:

            try:

                value = float(
                    amount.replace(",", "")
                )

                numeric_amounts.append(
                    value
                )

            except ValueError:
                continue

        if not numeric_amounts:
            return None

        # Usually the final amount is the balance
        balance = numeric_amounts[-1]

        # Second-last amount is generally
        # the transaction amount
        transaction_amount = (
            numeric_amounts[-2]
            if len(numeric_amounts) >= 2
            else 0.0
        )

        # Remove dates and amounts to create
        # a cleaner description
        description = text

        for date_value in dates:

            description = description.replace(
                date_value,
                ""
            )

        for amount in amounts:

            description = description.replace(
                amount,
                ""
            )

        description = " ".join(
            description.split()
        )

        if not description:
            return None

        transaction = {
            "date": transaction_date,
            "description": (
                TransactionCleaner
                .clean_description(
                    description
                )
            ),
            "debit": transaction_amount,
            "credit": 0.0,
            "balance": balance,
        }

        return CategoryEngine.categorize(
            transaction
        )