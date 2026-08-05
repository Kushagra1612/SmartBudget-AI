import Card from "../common/Card";

export default function SpendingOverview({
    categories = [],
}) {

    return (

        <Card>

            <h2 className="text-2xl font-bold">

                Spending Overview

            </h2>

            <p className="text-gray-500 mt-1">

                Top spending categories

            </p>

            <div className="mt-8 space-y-6">

                {categories.length === 0 ? (

                    <p className="text-gray-400">

                        No spending data available.

                    </p>

                ) : (

                    categories.map((item) => (

                        <div key={item.category}>

                            <div className="flex justify-between mb-2">

                                <span className="font-medium">

                                    {item.category}

                                </span>

                                <span className="font-semibold">

                                    ₹{Number(item.amount).toLocaleString("en-IN")}

                                </span>

                            </div>

                            <div className="h-3 rounded-full bg-gray-200">

                                <div
                                    className="h-full rounded-full bg-[var(--primary)]"
                                    style={{
                                        width: `${item.percentage}%`,
                                    }}
                                />

                            </div>

                        </div>

                    ))

                )}

            </div>

        </Card>

    );

}