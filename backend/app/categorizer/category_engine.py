from app.categorizer.fuzzy_matcher import FuzzyMatcher
from app.categorizer.payment_detector import PaymentDetector


class CategoryEngine:

    @staticmethod
    def categorize(transaction):

        merchant, category = FuzzyMatcher.find(
            transaction["description"]
        )

        payment = PaymentDetector.detect(
            transaction["description"]
        )

        if transaction["credit"] > 0:

            transaction_type = "Income"

        else:

            transaction_type = "Expense"

        transaction["merchant"] = merchant
        transaction["category"] = category
        transaction["payment_mode"] = payment
        transaction["transaction_type"] = transaction_type

        return transaction