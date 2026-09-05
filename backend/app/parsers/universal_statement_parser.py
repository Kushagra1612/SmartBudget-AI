import re
from datetime import datetime


class UniversalStatementParser:
    """
    Bank-agnostic parser for text extracted from PDF bank statements.

    The parser attempts to identify transactions using common patterns:
    - Transaction dates
    - Monetary values
    - Running balances
    - Transaction ordering

    It does not depend on a specific bank name or fixed statement layout.
    """

    DATE_REGEX = re.compile(
        r"\b("
        r"\d{2}/\d{2}/\d{2,4}|"
        r"\d{2}-\d{2}-\d{2,4}|"
        r"\d{4}-\d{2}-\d{2}"
        r")\b"
    )

    AMOUNT_REGEX = re.compile(
        r"(?<![\w/])"
        r"(?:₹|Rs\.?\s*)?"
        r"-?"
        r"(?:"
        r"\d{1,3}(?:,\d{3})+"
        r"|"
        r"\d+"
        r")"
        r"\.\d{2}"
        r"(?:\s*(?:CR|DR))?"
        r"(?!\w)",
        re.IGNORECASE,
    )

    DATE_FORMATS = [
        "%d/%m/%y",
        "%d/%m/%Y",
        "%d-%m-%y",
        "%d-%m-%Y",
        "%Y-%m-%d",
    ]

    # Footer/boilerplate keywords, matched against the line with ALL
    # whitespace and punctuation stripped out first. This sidesteps the
    # inconsistent spacing in PDF-extracted text (e.g. "GSTIN" running
    # directly into the next word with no space, or "This is a computer
    # generated statement" appearing with zero spaces at all) that made
    # word-boundary regexes unreliable. Add new phrases here as
    # lowercase, no-space/punctuation strings.
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
    def parse_date(cls, value: str):

        for date_format in cls.DATE_FORMATS:

            try:

                return datetime.strptime(
                    value,
                    date_format,
                ).date()

            except ValueError:
                continue

        return None

    @staticmethod
    def clean_amount(value: str) -> float:

        if not value:
            return 0.0

        cleaned = value.upper()

        cleaned = cleaned.replace("₹", "")
        cleaned = cleaned.replace("RS.", "")
        cleaned = cleaned.replace("RS", "")
        cleaned = cleaned.replace(",", "")
        cleaned = cleaned.replace("CR", "")
        cleaned = cleaned.replace("DR", "")
        cleaned = cleaned.strip()

        try:
            return float(cleaned)

        except ValueError:
            return 0.0

    @classmethod
    def is_transaction_start(
        cls,
        line: str,
    ) -> bool:

        match = re.match(
            r"^("
            r"\d{2}/\d{2}/\d{2,4}|"
            r"\d{2}-\d{2}-\d{2,4}|"
            r"\d{4}-\d{2}-\d{2}"
            r")\b",
            line,
        )

        if not match:
            return False

        parsed_date = cls.parse_date(
            match.group(1)
        )

        return parsed_date is not None

    @classmethod
    def is_footer_line(
        cls,
        line: str,
    ) -> bool:
        """
        True once we've reached statement boilerplate that comes after
        (or between) real transactions -- summary totals, legal
        notices, GST info, branch address, "computer generated
        statement" disclaimers, etc. Used to skip these lines so they
        never get glued onto a transaction's description.

        Punctuation and whitespace are stripped before matching,
        because PDF text extraction often squashes these phrases
        together with no spaces at all (e.g. "Thisisacomputergenerated
        statement"), which made word-boundary regexes unreliable.
        """

        squashed = re.sub(
            r"[^a-z0-9]",
            "",
            line.lower(),
        )

        return any(
            keyword in squashed
            for keyword in cls.FOOTER_KEYWORDS
        )

    @classmethod
    def split_transaction_blocks(
        cls,
        text: str,
    ) -> list[str]:

        lines = [
            " ".join(line.split())
            for line in text.splitlines()
            if line.strip()
        ]

        blocks = []

        current_block = []

        in_footer = False

        for line in lines:

            if cls.is_transaction_start(line):

                # A genuine transaction always resumes normal
                # processing, even if we were mid-footer.
                in_footer = False

                if current_block:

                    blocks.append(
                        " ".join(current_block)
                    )

                current_block = [line]

                continue

            if in_footer:

                # Already inside a footer/boilerplate section --
                # skip every line unconditionally until the next
                # real transaction starts. This handles footers
                # that span multiple physical PDF lines, even when
                # a single sentence is split mid-phrase across a
                # line break (which defeated a plain per-line
                # keyword check).
                continue

            if cls.is_footer_line(line):

                in_footer = True
                continue

            if current_block:

                current_block.append(line)

        if current_block:

            blocks.append(
                " ".join(current_block)
            )

        return blocks

    @classmethod
    def extract_description(
        cls,
        block: str,
        dates: list[str],
        amounts: list[str],
    ) -> str:

        description = block

        # Remove all dates.
        #
        # Statements often contain both transaction date
        # and value date.
        for date_value in dates:

            description = description.replace(
                date_value,
                "",
                1,
            )

        # Remove monetary values.
        for amount in amounts:

            description = description.replace(
                amount,
                "",
                1,
            )

        # Remove long numeric reference numbers.
        description = re.sub(
            r"\b\d{8,}\b",
            "",
            description,
        )

        # Remove common statement metadata.
        description = re.sub(
            r"\b(?:Page|PageNo|Account|Statement)\b.*",
            "",
            description,
            flags=re.IGNORECASE,
        )

        description = re.sub(
            r"\s+",
            " ",
            description,
        ).strip()

        # Safety net: even with footer detection above, cap description
        # length defensively so a future edge case can never crash the
        # DB insert again. The transactions.description column is
        # VARCHAR(500); stay comfortably under that.
        if len(description) > 480:
            description = description[:480].rstrip()

        return description

    @classmethod
    def parse_block(
        cls,
        block: str,
    ) -> dict | None:

        dates = cls.DATE_REGEX.findall(
            block
        )

        if not dates:
            return None

        transaction_date = cls.parse_date(
            dates[0]
        )

        if transaction_date is None:
            return None

        amounts = cls.AMOUNT_REGEX.findall(
            block
        )

        if len(amounts) < 2:
            return None

        cleaned_amounts = [
            cls.clean_amount(amount)
            for amount in amounts
        ]

        # Last amount is usually the running balance.
        balance = cleaned_amounts[-1]

        # Amount before balance is generally the
        # transaction amount.
        transaction_amount = cleaned_amounts[-2]

        if transaction_amount <= 0:
            return None

        description = cls.extract_description(
            block,
            dates,
            amounts,
        )

        if len(description) < 3:
            return None

        return {
            "date": transaction_date,
            "description": description,
            "amount": transaction_amount,
            "balance": balance,
        }

    @classmethod
    def infer_transaction_types(
        cls,
        transactions: list[dict],
    ) -> list[dict]:

        if not transactions:
            return []

        parsed_transactions = []

        for index, transaction in enumerate(
            transactions
        ):

            amount = transaction["amount"]
            current_balance = transaction["balance"]

            debit = 0.0
            credit = 0.0

            if index < len(transactions) - 1:

                next_balance = transactions[
                    index + 1
                ]["balance"]

                difference = (
                    next_balance
                    - current_balance
                )

                # Statements listed newest → oldest:
                #
                # Debit:
                # Older balance > current balance
                #
                # Credit:
                # Older balance < current balance

                if difference > 0:

                    debit = amount

                elif difference < 0:

                    credit = amount

                else:

                    # If balances are identical,
                    # use debit as a safe fallback.
                    debit = amount

            else:

                # Cannot reliably infer the final
                # transaction without another balance.
                debit = amount

            parsed_transactions.append(
                {
                    "date": transaction["date"],
                    "description": transaction[
                        "description"
                    ],
                    "debit": debit,
                    "credit": credit,
                    "balance": current_balance,
                }
            )

        return parsed_transactions

    @classmethod
    def remove_duplicates(
        cls,
        transactions: list[dict],
    ) -> list[dict]:

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

                unique_transactions.append(
                    transaction
                )

        return unique_transactions

    @classmethod
    def parse(
        cls,
        text: str,
    ) -> list[dict]:

        blocks = cls.split_transaction_blocks(
            text
        )

        parsed_transactions = []

        for block in blocks:

            transaction = cls.parse_block(
                block
            )

            if transaction is not None:

                parsed_transactions.append(
                    transaction
                )

        transactions = (
            cls.infer_transaction_types(
                parsed_transactions
            )
        )

        return cls.remove_duplicates(
            transactions
        )