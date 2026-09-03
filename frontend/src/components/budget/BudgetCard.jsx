import toast from "react-hot-toast";
import { deleteBudget } from "../../api/budget";

export default function BudgetCard({
    budget,
    onEdit,
    onDelete,
}) {

    const percentage = Math.min(
        budget.utilization_percentage,
        100,
    );

    async function handleDelete() {

        if (!confirm("Delete this budget?")) {
            return;
        }

        try {

            await deleteBudget(budget.id);

            onDelete(budget.id);

        } catch {

            toast.error("Failed to delete budget.");

        }

    }

    return (

        <div className="bg-white rounded-xl shadow p-6">

            <h2 className="text-xl font-bold">
                {budget.category}
            </h2>

            <p className="mt-3">
                ₹{budget.spent} / ₹{budget.monthly_limit}
            </p>

            <div className="w-full h-3 bg-gray-200 rounded-full mt-4">

                <div
                    className="bg-blue-500 h-3 rounded-full"
                    style={{
                        width: `${percentage}%`,
                    }}
                />

            </div>

            <p className="mt-2 text-sm text-gray-500">
                {percentage.toFixed(0)}%
            </p>

            <p className="mt-3">
                Remaining: ₹{budget.remaining}
            </p>

            <div className="flex gap-3 mt-6">

                <button
                    onClick={() => onEdit(budget)}
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