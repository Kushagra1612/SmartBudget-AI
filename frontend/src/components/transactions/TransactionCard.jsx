export default function TransactionCard({ transaction }) {

    const isIncome =
        transaction.transaction_type === "Income";

    return (

        <div
            className="
                bg-white
                rounded-2xl
                shadow
                p-5
                hover:shadow-lg
                transition
            "
        >

            <div className="flex justify-between items-start">

                <div>

                    <h3 className="text-lg font-semibold">
                        {transaction.merchant}
                    </h3>

                    <p className="text-sm text-gray-500 mt-1">
                        {transaction.description || "No description"}
                    </p>

                </div>

                <span
                    className={`
                        px-3
                        py-1
                        rounded-full
                        text-sm
                        font-medium
                        ${
                            isIncome
                                ? "bg-green-100 text-green-700"
                                : "bg-red-100 text-red-700"
                        }
                    `}
                >
                    {transaction.transaction_type}
                </span>

            </div>

            <div className="mt-5 flex justify-between">

                <div>

                    <p className="text-sm text-gray-500">
                        Category
                    </p>

                    <p className="font-medium">
                        {transaction.category}
                    </p>

                </div>

                <div>

                    <p className="text-sm text-gray-500">
                        Payment
                    </p>

                    <p className="font-medium">
                        {transaction.payment_mode || "-"}
                    </p>

                </div>

            </div>

            <div className="mt-5 flex justify-between items-end">

                <div>

                    <p className="text-sm text-gray-500">
                        Date
                    </p>

                    <p className="font-medium">
                        {transaction.transaction_date}
                    </p>

                </div>

                <p
                    className={`text-xl font-bold ${
                        isIncome
                            ? "text-green-600"
                            : "text-red-600"
                    }`}
                >
                    ₹{Number(transaction.amount).toLocaleString()}
                </p>

            </div>

        </div>

    );

}