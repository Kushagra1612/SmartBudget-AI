import { useState } from "react";
import { createGoal } from "../../api/goals";

export default function GoalForm({ onGoalCreated }) {

    const [form, setForm] = useState({
        title: "",
        target_amount: "",
        target_date: "",
    });

    const [loading, setLoading] = useState(false);

    function handleChange(e) {

        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });

    }

    async function handleSubmit(e) {

        e.preventDefault();

        try {

            setLoading(true);

            const goal = await createGoal({
                ...form,
                target_amount: Number(form.target_amount),
            });

            onGoalCreated(goal);

            setForm({
                title: "",
                target_amount: "",
                target_date: "",
            });

        } catch (err) {

            alert("Failed to create goal.");

        } finally {

            setLoading(false);

        }

    }

    return (

        <form
            onSubmit={handleSubmit}
            className="space-y-4 mb-8"
        >

            <input
                type="text"
                name="title"
                placeholder="Goal Title"
                value={form.title}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            <input
                type="number"
                name="target_amount"
                placeholder="Target Amount"
                value={form.target_amount}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            <input
                type="date"
                name="target_date"
                value={form.target_date}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            <button
                type="submit"
                disabled={loading}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg"
            >
                {loading ? "Creating..." : "Create Goal"}
            </button>

        </form>

    );

}