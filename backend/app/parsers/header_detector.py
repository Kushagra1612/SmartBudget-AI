import pandas as pd


class HeaderDetector:

    HEADER_KEYWORDS = {

        "date",
        "txn date",
        "transaction date",
        "value date",
        "narration",
        "description",
        "particulars",
        "debit",
        "withdrawal",
        "credit",
        "deposit",
        "balance",
        "closing balance",
        "running balance"

    }

    @staticmethod
    def detect(df: pd.DataFrame):

        for index in range(min(5, len(df))):

            row = df.iloc[index]

            values = [
                str(x).strip().lower()
                for x in row.values
            ]

            score = 0

            for value in values:

                if value in HeaderDetector.HEADER_KEYWORDS:
                    score += 1

            if score >= 2:

                df.columns = row

                df = df.iloc[index + 1:].reset_index(drop=True)

                return df

        return df