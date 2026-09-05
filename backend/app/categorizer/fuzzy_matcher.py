from rapidfuzz import process

from app.categorizer.merchant_loader import MerchantLoader


class FuzzyMatcher:

    @staticmethod
    def find(description):

        description = description.upper()

        merchants = MerchantLoader.load()

        merchant_names = []
        merchant_category = {}

        for category, names in merchants.items():

            for merchant in names:

                merchant_names.append(merchant)
                merchant_category[merchant] = category

        # Step 1: exact substring match.
        #
        # Real transaction descriptions are noisy (reference numbers,
        # bank codes, "-NOREMARK" suffixes, etc.), which drags down
        # WRatio's overall similarity score even when the merchant name
        # is literally, exactly present in the string -- e.g. "SWIGGY"
        # inside "UPI-SWIGGY-...-2-NOREMARK" scored only 60 despite
        # being a perfect substring match. Checking for a direct
        # substring first avoids these false negatives.
        #
        # When multiple merchant names are substrings (e.g. both
        # "SWIGGY" and "SWIGGY INSTAMART" could match), prefer the
        # longest match, since it's the most specific.
        substring_matches = [
            merchant
            for merchant in merchant_names
            if merchant in description
        ]

        if substring_matches:

            merchant = max(
                substring_matches,
                key=len,
            )

            return merchant, merchant_category[merchant]

        # Step 2: fall back to fuzzy matching for typos/variations
        # that aren't an exact substring (e.g. OCR errors, unusual
        # bank formatting).
        match = process.extractOne(
            description,
            merchant_names,
            score_cutoff=70,
        )

        if match:

            merchant = match[0]

            return merchant, merchant_category[merchant]

        return "UNKNOWN", "Others"