import { useState } from "react";
import toast from "react-hot-toast";
import { deleteGoal, contributeToGoal } from "../../api/goals";

export default function GoalCard({
    goal,
    onDelete,
    onEdit,
    onContribute,
}) {

    const [showContributeForm, setShowContributeForm] = useState(false);
    const [amount, setAmount] = useState("");
    const [submitting, setSubmitting] = useState(false);

    // Prefer the live progress fields the backend now computes
    // (progress_percentage, remaining, days_left) -- fall back to a
    // local calculation only if an older cached goal object doesn't
    // have them yet.
    const percentage = Math.min(
        goal.progress_percentage ??
            (goal.current_amount / goal.target_amount) * 100,
        100,
    );

    const remaining =
        goal.remaining ?? goal.target_amount - goal.current_amount;

    async function handleDelete() {

        if (!confirm("Delete this goal?")) return;

        try {

            await deleteGoal(goal.id);

            onDelete(goal.id);

        } catch {

            toast.error("Failed to delete goal.");

        }

    }

    async function handleContribute(e) {

        e.preventDefault();

        const numericAmount = Number(amount);

        if (!numericAmount || numericAmount <= 0) {

            toast.error("Enter an amount greater than 0.");

            return;

        }

        try {

            setSubmitting(true);

            const updatedGoal = await contributeToGoal(
                goal.id,
                numericAmount,
            );

            onContribute(updatedGoal);

            toast.success(`Added ₹${numericAmount} to ${goal.title}.`);

            setAmount("");
            setShowContributeForm(false);

        } catch {

            toast.error("Failed to add contribution.");

        } finally {

            setSubmitting(false);

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
                {goal.days_left != null && (
                    <span className="ml-2">
                        · ₹{remaining} left · {goal.days_left} days left
                    </span>
                )}
            </p>

            <p className="mt-3 text-sm">
                Target: {goal.target_date}
            </p>

            {showContributeForm ? (

                <form
                    onSubmit={handleContribute}
                    className="flex gap-2 mt-5"
                >

                    <input
                        type="number"
                        min="1"
                        step="0.01"
                        autoFocus
                        placeholder="Amount"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
                    />

                    <button
                        type="submit"
                        disabled={submitting}
                        className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
                    >
                        {submitting ? "..." : "Add"}
                    </button>

                    <button
                        type="button"
                        onClick={() => {

                            setShowContributeForm(false);

                            setAmount("");

                        }}
                        className="bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded-lg"
                    >
                        Cancel
                    </button>

                </form>

            ) : (

                <button
                    onClick={() => setShowContributeForm(true)}
                    className="w-full mt-5 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg"
                >
                    + Add Money
                </button>

            )}

            <div className="flex gap-3 mt-3">

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