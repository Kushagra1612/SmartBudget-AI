class BankIdentifier:

    @staticmethod
    def identify(text: str):

        text = text.upper()

        if "STATE BANK OF INDIA" in text:
            return "SBI"

        if "HDFC BANK" in text:
            return "HDFC"

        if "ICICI BANK" in text:
            return "ICICI"

        if "AXIS BANK" in text:
            return "AXIS"

        if "PUNJAB NATIONAL BANK" in text:
            return "PNB"

        return "UNKNOWN"