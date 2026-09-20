import Card from "../common/Card";
import useBudgetSummary from "../../hooks/useBudgetSummary";
import { formatRupees } from "../../utils/currency";

function getBarColor(utilization) {

    if (utilization >= 100) return "var(--danger)";
    if (utilization >= 70) return "var(--warning)";

    return "var(--success)";

}

export default function BudgetOverviewCard() {

    const {
        summary,
        loading,
        error,
    } = useBudgetSummary();

    return (

        <Card>

            <h2 className="text-2xl font-bold">
                Budgets
            </h2>

            <p className="text-gray-500 mt-1">
                This month's budget usage
            </p>

            {loading ? (

                <p className="text-gray-400 mt-8">
                    Loading budgets...
                </p>

            ) : error ? (

                <p className="text-red-500 mt-8">
                    Failed to load budgets.
                </p>

            ) : summary.length === 0 ? (

                <p className="text-gray-400 mt-8">
                    No budgets set yet. Create one to track your spending limits.
                </p>

            ) : (

                <div className="mt-8 space-y-6">

                    {summary.map((budget) => {

                        const utilization = budget.utilization_percentage;
                        const overBudget = utilization >= 100;
                        const barColor = getBarColor(utilization);

                        return (

                            <div key={budget.id}>

                                <div className="flex justify-between mb-2">

                                    <span className="font-medium">
                                        {budget.category}
                                    </span>

                                    <span className="font-semibold">
                                        {formatRupees(budget.spent)} / {formatRupees(budget.monthly_limit)}
                                    </span>

                                </div>

                                <div className="h-3 rounded-full bg-gray-200">

                                    <div
                                        className="h-full rounded-full transition-all"
                                        style={{
                                            width: `${Math.min(utilization, 100)}%`,
                                            backgroundColor: barColor,
                                        }}
                                    />

                                </div>

                                {overBudget && (

                                    <p className="text-xs mt-1 font-medium" style={{ color: "var(--danger)" }}>
                                        Over budget by {formatRupees(budget.spent - budget.monthly_limit)}
                                    </p>

                                )}

                            </div>

                        );

                    })}

                </div>

            )}

        </Card>

    );

}