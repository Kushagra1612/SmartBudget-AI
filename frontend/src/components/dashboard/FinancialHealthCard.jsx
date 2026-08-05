import Card from "../common/Card";

export default function FinancialHealthCard({
    score,
    grade,
    status,
}) {
    return (
        <Card className="flex flex-col items-center text-center">

            <p className="text-gray-500 font-medium">
                Financial Health
            </p>

            <div className="mt-6 w-40 h-40 rounded-full border-8 border-[var(--primary)] flex items-center justify-center">

                <div>

                    <h1 className="text-5xl font-bold">
                        {score}
                    </h1>

                    <p className="text-sm text-gray-500">
                        {grade}
                    </p>

                </div>

            </div>

            <p
                className={`mt-6 font-semibold ${
                    score >= 80
                        ? "text-green-600"
                        : score >= 60
                        ? "text-yellow-500"
                        : "text-red-500"
                }`}
            >
                {status}
            </p>

        </Card>
    );
}