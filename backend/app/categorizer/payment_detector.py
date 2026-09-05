import re


class PaymentDetector:

    # Google Pay registers "@ok<bankname>" handles across every
    # partner bank (e.g. @okicici, @okaxis, @oksbi, @okhdfcbank) --
    # this prefix is specific to GPay regardless of which bank the
    # user actually banks with.
    GPAY_HANDLE_PATTERN = re.compile(r"OK[A-Z]{3,15}")

    # PhonePe registers UPI handles under these bank codes (Yes Bank
    # Ltd / ICICI Bank Ltd / Axis Bank Ltd) across ALL its users,
    # again regardless of which bank the user actually banks with.
    # Matched with boundaries so we don't false-positive on the
    # substring appearing inside an unrelated word.
    PHONEPE_HANDLE_PATTERN = re.compile(
        r"(?<![A-Z])(?:YBL|IBL|AXL)(?![A-Z])"
    )

    @staticmethod
    def detect(description):

        desc = description.upper()

        # Check specific UPI apps/PSPs BEFORE the generic "UPI" check
        # below. Almost every transaction description already contains
        # the literal word "UPI" (e.g. "UPI-SWIGGY-..."), so if the
        # generic check ran first it would always match and return
        # immediately -- these more specific checks would never be
        # reached.
        if "BHIM" in desc:
            return "BHIM"

        if "GPAY" in desc or "GOOGLE PAY" in desc:
            return "GPAY"

        if "PHONEPE" in desc:
            return "PHONEPE"

        if "PAYTM" in desc:
            return "PAYTM"

        if "MOBIKWIK" in desc:
            return "MOBIKWIK"

        if "SLICE" in desc:
            return "SLICE"

        if "SUPERMONEY" in desc:
            return "SUPERMONEY"

        if "PAYZAPP" in desc:
            return "PAYZAPP"

        if "NAVI" in desc:
            return "NAVI"

        if "AMAZON PAY" in desc or "AMAZONPAY" in desc:
            return "AMAZON PAY"

        # Heuristic fallback: infer the app from the UPI handle when
        # the app name itself isn't spelled out anywhere in the
        # description (this is the common case -- most descriptions
        # only show the bank/PSP handle, not the consumer app name).
        #
        # Match against a whitespace-stripped version, since PDF text
        # extraction sometimes wraps mid-word and inserts a stray
        # space in the middle of a handle (e.g. "OKAXIS" -> "OKAX IS",
        # "AXL" -> "A XL"), which would otherwise defeat these
        # patterns.
        #
        # This is a best-effort inference, not a certainty: handles
        # can theoretically be reused or misattributed, so treat this
        # as "most likely app", not a guaranteed fact.
        squashed = re.sub(r"\s+", "", desc)

        if PaymentDetector.GPAY_HANDLE_PATTERN.search(squashed):
            return "GPAY"

        if PaymentDetector.PHONEPE_HANDLE_PATTERN.search(squashed):
            return "PHONEPE"

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