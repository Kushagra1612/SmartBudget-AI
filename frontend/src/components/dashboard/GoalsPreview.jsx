import Card from "../common/Card";
import useGoals from "../../hooks/useGoals";

export default function GoalsPreview() {

    const {
        goals,
        loading,
        error,
    } = useGoals();

    if (loading) {
        return (
            <Card>
                Loading goals...
            </Card>
        );
    }

    if (error) {
        return (
            <Card>
                Unable to load goals.
            </Card>
        );
    }

    return (

        <Card>

            <div className="flex justify-between items-center">

                <h2 className="text-2xl font-bold">
                    Goals
                </h2>

                <button className="text-sm text-[var(--primary)]">

                    View All

                </button>

            </div>

            <div className="mt-6 space-y-6">

                {goals.length === 0 && (

                    <p className="text-gray-500">

                        No goals created yet.

                    </p>

                )}

                {goals.slice(0, 3).map(goal => {

                    const progress = Math.min(
                        (Number(goal.current_amount) /
                            Number(goal.target_amount)) * 100,
                        100
                    );

                    return (

                        <div key={goal.id}>

                            <div className="flex justify-between">

                                <div>

                                    <h3 className="font-semibold">

                                        {goal.title}

                                    </h3>

                                    <p className="text-sm text-gray-500">

                                        ₹{Number(goal.current_amount).toLocaleString("en-IN")}
                                        {" / "}
                                        ₹{Number(goal.target_amount).toLocaleString("en-IN")}

                                    </p>

                                </div>

                                <span className="font-semibold">

                                    {progress.toFixed(0)}%

                                </span>

                            </div>

                            <div className="mt-3 h-2 bg-gray-200 rounded-full">

                                <div
                                    className="h-2 rounded-full bg-[var(--primary)] transition-all duration-500"
                                    style={{
                                        width: `${progress}%`,
                                    }}
                                />

                            </div>

                            <div className="flex justify-between mt-2 text-xs text-gray-500">

                                <span>

                                    {goal.status}

                                </span>

                                <span>

                                    {goal.target_date}

                                </span>

                            </div>

                        </div>

                    );

                })}

            </div>

        </Card>

    );

}