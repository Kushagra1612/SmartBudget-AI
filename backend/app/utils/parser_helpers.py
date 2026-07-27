import pandas as pd


class ParserHelper:

    @staticmethod
    def normalize_columns(df: pd.DataFrame):

        mapping = {
            "date": "date",
            "txn date": "date",
            "tran date": "date",
            "transaction date": "date",
            "value date": "date",

            "narration": "description",
            "description": "description",
            "particulars": "description",

            "withdrawal": "debit",
            "withdrawal amt.": "debit",
            "withdrawal amount": "debit",
            "debit": "debit",
            "dr": "debit",

            "deposit": "credit",
            "deposit amt.": "credit",
            "deposit amount": "credit",
            "credit": "credit",
            "cr": "credit",

            "balance": "balance",
            "closing balance": "balance",
            "running balance": "balance",
            "available balance": "balance",
        }

        columns = {}

        for column in df.columns:

            # Normalize the original column name
            original = str(column).strip()
            lookup = original.lower()

            if lookup in mapping:
                columns[column] = mapping[lookup]
            else:
                columns[column] = lookup

        return df.rename(columns=columns)