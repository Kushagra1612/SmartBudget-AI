import { useEffect, useState } from "react";

import MainLayout from "../layouts/MainLayout";
import useGoals from "../hooks/useGoals";
import GoalCard from "../components/goals/GoalCard";
import GoalForm from "../components/goals/GoalForm";

export default function Goals() {

    const {
        goals,
        loading,
        error,
    } = useGoals();

    const [goalList, setGoalList] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [editingGoal, setEditingGoal] = useState(null);

    useEffect(() => {
        setGoalList(goals);
    }, [goals]);

    function removeGoal(id) {

        setGoalList((prev) =>
            prev.filter((goal) => goal.id !== id)
        );

    }

    function addGoal(goal) {

        setGoalList((prev) => [
            goal,
            ...prev,
        ]);

    }

    function editGoal(goal) {

        setEditingGoal(goal);
        setShowForm(true);

    }

    function updateExistingGoal(updatedGoal) {

        setGoalList((prev) =>
            prev.map((goal) =>
                goal.id === updatedGoal.id
                    ? updatedGoal
                    : goal
            )
        );

    }

    if (loading) {
        return <p>Loading goals...</p>;
    }

    if (error) {
        return <p>Error loading goals.</p>;
    }

    return (

        <MainLayout>

            <div className="flex justify-between items-center mb-8">

                <h1 className="text-3xl font-bold">
                    My Goals
                </h1>

                <button
                    onClick={() => {

                        setEditingGoal(null);
                        setShowForm(true);

                    }}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-lg transition"
                >
                    + Add Goal
                </button>

            </div>

            {showForm && (

                <GoalForm
                    goal={editingGoal}
                    onGoalCreated={(goal) => {

                        addGoal(goal);

                        setShowForm(false);

                    }}
                    onGoalUpdated={(goal) => {

                        updateExistingGoal(goal);

                        setEditingGoal(null);

                        setShowForm(false);

                    }}
                />

            )}

            {goalList.length === 0 ? (

                <div className="text-center py-20 text-gray-500">

                    <p className="text-xl">
                        No goals found.
                    </p>

                    <p className="mt-2">
                        Click <strong>+ Add Goal</strong> to create your first goal.
                    </p>

                </div>

            ) : (

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                    {goalList.map((goal) => (

                        <GoalCard
                            key={goal.id}
                            goal={goal}
                            onDelete={removeGoal}
                            onEdit={editGoal}
                        />

                    ))}

                </div>

            )}

        </MainLayout>

    );

}