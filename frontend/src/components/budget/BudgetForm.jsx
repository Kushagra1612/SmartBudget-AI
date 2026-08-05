import { useEffect, useState } from "react";

import {
    createBudget,
    updateBudget,
} from "../../api/budget";

import { TRANSACTION_CATEGORIES } from "../../constants/categories";

export default function BudgetForm({
    budget = null,
    onBudgetCreated,
    onBudgetUpdated,
}) {

    const currentDate = new Date();

    const [form, setForm] = useState({
        category: "",
        monthly_limit: "",
        month: currentDate.getMonth() + 1,
        year: currentDate.getFullYear(),
    });

    const [loading, setLoading] = useState(false);

    useEffect(() => {

        if (budget) {

            setForm({
                category: budget.category,
                monthly_limit: budget.monthly_limit,
                month: budget.month,
                year: budget.year,
            });

        } else {

            setForm({
                category: "",
                monthly_limit: "",
                month: currentDate.getMonth() + 1,
                year: currentDate.getFullYear(),
            });

        }

    }, [budget]);

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

            if (budget) {

                const updated = await updateBudget(
                    budget.id,
                    {
                        category: form.category,
                        monthly_limit: Number(form.monthly_limit),
                    }
                );

                onBudgetUpdated(updated);

            } else {

                const created = await createBudget({
                    category: form.category,
                    monthly_limit: Number(form.monthly_limit),
                    month: Number(form.month),
                    year: Number(form.year),
                });

                onBudgetCreated(created);

                setForm({
                    category: "",
                    monthly_limit: "",
                    month: currentDate.getMonth() + 1,
                    year: currentDate.getFullYear(),
                });

            }

        } catch (err) {

            alert(
                budget
                    ? "Failed to update budget."
                    : "Failed to create budget."
            );

        } finally {

            setLoading(false);

        }

    }

    return (

        <form
            onSubmit={handleSubmit}
            className="space-y-4 mb-8"
        >

            <select
                name="category"
                value={form.category}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            >

                <option value="">
                    Select Category
                </option>

                {TRANSACTION_CATEGORIES.map((category) => (

                    <option
                        key={category}
                        value={category}
                    >
                        {category}
                    </option>

                ))}

            </select>

            <input
                type="number"
                name="monthly_limit"
                placeholder="Monthly Limit"
                value={form.monthly_limit}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            <button
                type="submit"
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition"
            >
                {loading
                    ? (budget ? "Updating..." : "Creating...")
                    : (budget ? "Update Budget" : "Create Budget")}
            </button>

        </form>

    );

}