import { useState } from "react";
import { Target, IndianRupee, Calendar } from "lucide-react";
import toast from "react-hot-toast";
import {
    createGoal,
    updateGoal,
} from "../../api/goals";
import Button from "../common/Button";
import Input from "../common/Input";
import Badge from "../common/Badge";

export default function GoalForm({
    goal = null,
    onGoalCreated,
    onGoalUpdated,
}) {

    const [form, setForm] = useState({
        title: goal?.title ?? "",
        target_amount: goal?.target_amount ?? "",
        target_date: goal?.target_date ?? "",
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

            if (goal) {

                const updated = await updateGoal(
                    goal.id,
                    {
                        ...form,
                        target_amount: Number(form.target_amount),
                    }
                );

                onGoalUpdated(updated);

            } else {

                const created = await createGoal({
                    ...form,
                    target_amount: Number(form.target_amount),
                });

                onGoalCreated(created);

                setForm({
                    title: "",
                    target_amount: "",
                    target_date: "",
                });

            }

        } catch {

            toast.error(
                goal
                    ? "Failed to update goal."
                    : "Failed to create goal."
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

            {goal && (
                <Badge color="primary">
                    Editing {goal.title}
                </Badge>
            )}

            <Input
                type="text"
                name="title"
                placeholder="Goal Title"
                value={form.title}
                onChange={handleChange}
                icon={Target}
                required
            />

            <Input
                type="number"
                name="target_amount"
                placeholder="Target Amount"
                value={form.target_amount}
                onChange={handleChange}
                icon={IndianRupee}
                required
            />

            <Input
                type="date"
                name="target_date"
                value={form.target_date}
                onChange={handleChange}
                icon={Calendar}
                required
            />

            <Button
                type="submit"
                disabled={loading}
            >
                {loading
                    ? (goal ? "Updating..." : "Creating...")
                    : (goal ? "Update Goal" : "Create Goal")}
            </Button>

        </form>

    );

}