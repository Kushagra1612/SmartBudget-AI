import Card from "../common/Card";

export default function FinancialHealthCard() {
    return (
        <Card className="flex flex-col items-center text-center">

            <p className="text-gray-500 font-medium">
                Financial Health
            </p>

            <div className="mt-6 w-40 h-40 rounded-full border-8 border-[var(--primary)] flex items-center justify-center">

                <div>

                    <h1 className="text-5xl font-bold">
                        87
                    </h1>

                    <p className="text-sm text-gray-500">
                        Excellent
                    </p>

                </div>

            </div>

            <p className="mt-6 text-green-600 font-semibold">

                +5 since last month

            </p>

        </Card>
    );
}