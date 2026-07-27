import re

DATE = re.compile(
    r"\d{2}[/-]\d{2}[/-]\d{2,4}"
)

AMOUNT = re.compile(
    r"[-₹,0-9]+\.\d{2}"
)

UPI = re.compile(
    r"UPI",
    re.I
)

NEFT = re.compile(
    r"NEFT",
    re.I
)

IMPS = re.compile(
    r"IMPS",
    re.I
)

ATM = re.compile(
    r"ATM",
    re.I
)