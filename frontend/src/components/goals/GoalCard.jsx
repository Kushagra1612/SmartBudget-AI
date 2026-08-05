import { deleteGoal } from "../../api/goals";

export default function GoalCard({ goal, onDelete }) {

    const percentage = Math.min(
        (goal.current_amount / goal.target_amount) * 100,
        100,
    );

    async function handleDelete() {

        if (!confirm("Delete this goal?")) return;

        await deleteGoal(goal.id);

        onDelete(goal.id);
    }

    return (

        <div className="bg-white rounded-xl shadow p-6">

            <h2 className="text-xl font-bold">
                {goal.title}
            </h2>

            <p className="mt-3">
                ₹{goal.current_amount} / ₹{goal.target_amount}
            </p>

            <div className="w-full h-3 bg-gray-200 rounded-full mt-4">

                <div
                    className="bg-green-500 h-3 rounded-full"
                    style={{
                        width: `${percentage}%`,
                    }}
                />

            </div>

            <p className="mt-2 text-sm text-gray-500">
                {percentage.toFixed(0)}%
            </p>

            <p className="mt-3 text-sm">
                Target:
                {" "}
                {goal.target_date}
            </p>

            <button
                onClick={handleDelete}
                className="mt-5 bg-red-500 text-white px-4 py-2 rounded"
            >
                Delete
            </button>

        </div>

    );

}