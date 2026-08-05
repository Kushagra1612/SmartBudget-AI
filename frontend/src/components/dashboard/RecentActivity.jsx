import Card from "../common/Card";

export default function RecentActivity({
    transactions = [],
}) {

    return (

        <Card>

            <h2 className="text-2xl font-bold">
                Recent Activity
            </h2>

            <div className="mt-6 space-y-4">

                {transactions.length === 0 ? (

                    <p className="text-gray-400">
                        No recent transactions.
                    </p>

                ) : (

                    transactions.map((transaction) => (

                        <div
                            key={transaction.id}
                            className="flex justify-between items-center border-b pb-3"
                        >

                            <div>

                                <h3 className="font-semibold">

                                    {transaction.merchant}

                                </h3>

                                <p className="text-sm text-gray-500">

                                    {transaction.category}

                                </p>

                            </div>

                            <div className="text-right">

                                <p
                                    className={`font-bold ${
                                        transaction.transaction_type === "EXPENSE"
                                            ? "text-red-500"
                                            : "text-green-600"
                                    }`}
                                >

                                    ₹{Number(transaction.amount).toLocaleString("en-IN")}

                                </p>

                                <p className="text-xs text-gray-400">

                                    {transaction.transaction_date}

                                </p>

                            </div>

                        </div>

                    ))

                )}

            </div>

        </Card>

    );

}