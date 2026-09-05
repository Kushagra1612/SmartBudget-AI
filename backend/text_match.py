from app.categorizer.fuzzy_matcher import FuzzyMatcher

test_descriptions = [
    "UPI-SWIGGY-UPISWIGGY@ICICI-ICIC0DC0099-2 -NOREMARK",
    "UPI-ZOMATO-ZOMATO.ETERNALTSP.PAYU@HDFCBA NK-HDFC0MERUPI--UPIINTENT",
    "UPI-SWIGGY INSTAMART-SWIGGYINSTAMARTECOM @ICICI-ICIC0DC0099--NOREMAR K",
]

for desc in test_descriptions:
    merchant, category = FuzzyMatcher.find(desc)
    print(f"{desc!r} -> merchant={merchant}, category={category}")