import toast from "react-hot-toast";
import { deleteGoal } from "../../api/goals";

export default function GoalCard({
    goal,
    onDelete,
    onEdit,
}) {

    const percentage = Math.min(
        (goal.current_amount / goal.target_amount) * 100,
        100,
    );

    async function handleDelete() {

        if (!confirm("Delete this goal?")) return;

        try {

            await deleteGoal(goal.id);

            onDelete(goal.id);

        } catch {

            toast.error("Failed to delete goal.");

        }

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
                Target: {goal.target_date}
            </p>

            <div className="flex gap-3 mt-5">

                <button
                    onClick={() => onEdit(goal)}
                    className="flex-1 bg-yellow-500 hover:bg-yellow-600 text-white py-2 rounded-lg"
                >
                    Edit
                </button>

                <button
                    onClick={handleDelete}
                    className="flex-1 bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg"
                >
                    Delete
                </button>

            </div>

        </div>

    );

}