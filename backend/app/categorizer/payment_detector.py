class PaymentDetector:

    @staticmethod
    def detect(description):

        desc = description.upper()

        if "UPI" in desc:
            return "UPI"

        if "NEFT" in desc:
            return "NEFT"

        if "IMPS" in desc:
            return "IMPS"

        if "ATM" in desc:
            return "ATM"

        if "POS" in desc:
            return "CARD"

        if "CHEQUE" in desc:
            return "CHEQUE"

        return "OTHER"