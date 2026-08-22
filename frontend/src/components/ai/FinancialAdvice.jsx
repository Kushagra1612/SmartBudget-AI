import Card from "../common/Card";
import useFinancialAdvice from "../../hooks/useFinancialAdvice";

export default function FinancialAdvice() {

    const {
        advice,
        agentsUsed,
        loading,
    } = useFinancialAdvice();

    if (loading) {
        return (
            <Card>
                <h2 className="text-2xl font-bold">
                    Financial Advice
                </h2>

                <p className="mt-4 text-gray-500">
                    Generating personalized advice...
                </p>
            </Card>
        );
    }

    return (

        <Card>

            <h2 className="text-2xl font-bold">
                💡 Monthly Financial Advice
            </h2>

            <div className="mt-6 whitespace-pre-line text-gray-700 leading-7">

                {advice}

            </div>

            {agentsUsed && agentsUsed.length > 0 && (

                <p className="mt-4 text-xs text-gray-400">
                    Consulted:{" "}
                    {agentsUsed
                        .map((a) => a.charAt(0).toUpperCase() + a.slice(1))
                        .join(", ")}
                </p>

            )}

        </Card>

    );

}