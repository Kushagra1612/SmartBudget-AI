import { useEffect, useState } from "react";
import { IndianRupee } from "lucide-react";

import {
    createBudget,
    updateBudget,
} from "../../api/budget";

import { TRANSACTION_CATEGORIES } from "../../constants/categories";
import Button from "../common/Button";
import Input from "../common/Input";
import Badge from "../common/Badge";

export default function BudgetForm({
    budget = null,
    onBudgetCreated,
    onBudgetUpdated,
}) {

    const [form, setForm] = useState({
        category: "",
        monthly_limit: "",
    });

    const [loading, setLoading] = useState(false);

    useEffect(() => {

        if (budget) {

            setForm({
                category: budget.category,
                monthly_limit: budget.monthly_limit,
            });

        } else {

            setForm({
                category: "",
                monthly_limit: "",
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
                });

                onBudgetCreated(created);

                setForm({
                    category: "",
                    monthly_limit: "",
                });

            }

        } catch {

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

            {budget && (
                <Badge color="primary">
                    Editing {budget.category}
                </Badge>
            )}

            <select
                name="category"
                value={form.category}
                onChange={handleChange}
                className="w-full bg-white border border-gray-200 rounded-2xl px-4 py-3 shadow-sm outline-none focus:border-[var(--primary)] transition-all"
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

            <Input
                type="number"
                name="monthly_limit"
                placeholder="Monthly Limit"
                value={form.monthly_limit}
                onChange={handleChange}
                icon={IndianRupee}
                required
            />

            <Button
                type="submit"
                disabled={loading}
            >
                {loading
                    ? (budget ? "Updating..." : "Creating...")
                    : (budget ? "Update Budget" : "Create Budget")}
            </Button>

        </form>

    );

}