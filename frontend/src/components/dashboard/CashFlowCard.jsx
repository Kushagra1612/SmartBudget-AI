import Card from "../common/Card";

export default function CashFlowCard({
    title,
    amount,
    change,
    positive = true,
}) {
    return (
        <Card>

            <p className="text-gray-500 font-medium">
                {title}
            </p>

            <h2 className="text-3xl font-bold mt-3">
                ₹{amount}
            </h2>

            <p
                className={`mt-3 font-semibold ${
                    positive
                        ? "text-green-600"
                        : "text-red-500"
                }`}
            >
                {change}
            </p>

        </Card>
    );
}