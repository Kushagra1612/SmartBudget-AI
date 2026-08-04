import Card from "../common/Card";

const spendingData = [
    {
        category: "Food",
        amount: 13200,
        percentage: 82,
        color: "bg-orange-400",
    },
    {
        category: "Shopping",
        amount: 7500,
        percentage: 55,
        color: "bg-indigo-500",
    },
    {
        category: "Travel",
        amount: 3200,
        percentage: 32,
        color: "bg-teal-500",
    },
    {
        category: "Entertainment",
        amount: 1800,
        percentage: 18,
        color: "bg-pink-500",
    },
];

export default function SpendingOverview() {
    return (
        <Card>

            <h2 className="text-2xl font-bold">
                Spending Overview
            </h2>

            <p className="text-gray-500 mt-1">
                Top spending categories
            </p>

            <div className="mt-8 space-y-6">

                {spendingData.map((item) => (

                    <div key={item.category}>

                        <div className="flex justify-between mb-2">

                            <span className="font-medium">
                                {item.category}
                            </span>

                            <span className="font-semibold">
                                ₹{item.amount.toLocaleString()}
                            </span>

                        </div>

                        <div className="h-3 rounded-full bg-gray-200">

                            <div
                                className={`${item.color} h-full rounded-full`}
                                style={{
                                    width: `${item.percentage}%`,
                                }}
                            />

                        </div>

                    </div>

                ))}

            </div>

        </Card>
    );
}