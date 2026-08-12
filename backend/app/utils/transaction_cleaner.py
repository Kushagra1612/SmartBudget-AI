import re
from datetime import datetime, date


class TransactionCleaner:

    @staticmethod
    def clean_amount(value):

        if value is None:
            return 0.0

        value = str(value)

        value = value.replace("₹", "")
        value = value.replace(",", "")
        value = value.strip()

        if value == "":
            return 0.0

        try:
            return float(value)

        except Exception:
            return 0.0

    @staticmethod
    def clean_description(text):

        if text is None:
            return ""

        text = str(text)

        text = text.replace("/", " ")
        text = text.replace("-", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip().upper()

    @staticmethod
    def clean_date(date_string) -> date | None:

        if date_string is None:
            return None

        date_string = str(date_string).strip()

        formats = [

            "%d/%m/%Y",
            "%d/%m/%y",
            "%d-%m-%Y",
            "%d-%m-%y",

        ]

        for fmt in formats:

            try:

                return datetime.strptime(
                    date_string,
                    fmt,
                ).date()

            except Exception:
                continue

        return None