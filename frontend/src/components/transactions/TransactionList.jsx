import useTransactions from "../../hooks/useTransactions";
import TransactionCard from "./TransactionCard";

export default function TransactionList({
    search,
    category,
    type,
}) {

    const {
        transactions,
        loading,
        error,
    } = useTransactions();

    if (loading) {
        return (
            <p className="mt-10 text-center">
                Loading transactions...
            </p>
        );
    }

    if (error) {
        return (
            <p className="mt-10 text-center text-red-500">
                Failed to load transactions.
            </p>
        );
    }

    const filteredTransactions = transactions.filter((transaction) => {

        const matchesSearch =
            search === "" ||
            transaction.merchant
                ?.toLowerCase()
                .includes(search.toLowerCase()) ||
            transaction.description
                ?.toLowerCase()
                .includes(search.toLowerCase());

        const matchesCategory =
            category === "" ||
            transaction.category === category;

        const matchesType =
            type === "" ||
            transaction.transaction_type === type;

        return (
            matchesSearch &&
            matchesCategory &&
            matchesType
        );

    });

    if (filteredTransactions.length === 0) {

        return (

            <div className="mt-16 text-center">

                <h2 className="text-2xl font-semibold">
                    No matching transactions
                </h2>

                <p className="text-gray-500 mt-3">
                    Try changing your search or filters.
                </p>

            </div>

        );

    }

    return (

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">

            {filteredTransactions.map((transaction) => (

                <TransactionCard
                    key={transaction.id}
                    transaction={transaction}
                />

            ))}

        </div>

    );

}