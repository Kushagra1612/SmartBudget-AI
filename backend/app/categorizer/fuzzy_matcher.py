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

        match = process.extractOne(
            description,
            merchant_names,
            score_cutoff=70,
        )

        if match:

            merchant = match[0]

            return merchant, merchant_category[merchant]

        return "UNKNOWN", "Others"