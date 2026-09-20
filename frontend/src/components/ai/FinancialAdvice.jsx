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

                <p className="mt-4 text-[var(--text-light)]">
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

            <div className="mt-6 whitespace-pre-line text-[var(--text)] leading-7">

                {advice}

            </div>

            {agentsUsed && agentsUsed.length > 0 && (

                <p className="mt-4 text-xs text-[var(--text-light)]">
                    Consulted:{" "}
                    {agentsUsed
                        .map((a) => a.charAt(0).toUpperCase() + a.slice(1))
                        .join(", ")}
                </p>

            )}

        </Card>

    );

}