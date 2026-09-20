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

                    <p className="text-[var(--text-light)]">
                        No recent transactions.
                    </p>

                ) : (

                    transactions.map((transaction) => (

                        <div
                            key={transaction.id}
                            className="flex justify-between items-center border-b border-[var(--border)] pb-3"
                        >

                            <div>

                                <h3 className="font-semibold">

                                    {transaction.merchant}

                                </h3>

                                <p className="text-sm text-[var(--text-light)]">

                                    {transaction.category}

                                </p>

                            </div>

                            <div className="text-right">

                                <p
                                    className={`font-bold ${
                                        transaction.transaction_type === "Expense"
                                            ? "text-red-500"
                                            : "text-green-600"
                                    }`}
                                >

                                    ₹{Number(transaction.amount).toLocaleString("en-IN")}

                                </p>

                                <p className="text-xs text-[var(--text-light)]">

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