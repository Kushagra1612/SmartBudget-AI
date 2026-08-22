import { useState } from "react";

import MainLayout from "../layouts/MainLayout";
import BudgetForm from "../components/budget/BudgetForm";
import BudgetCard from "../components/budget/BudgetCard";
import useBudgetSummary from "../hooks/useBudgetSummary";

export default function Budget() {

    const {
        summary,
        loading,
        error,
        refetch,
    } = useBudgetSummary();

    const [showForm, setShowForm] = useState(false);
    const [editingBudget, setEditingBudget] = useState(null);

    function removeBudget() {

        refetch();

        setEditingBudget(null);
        setShowForm(false);

    }

    function editBudget(budget) {

        setEditingBudget(budget);
        setShowForm(true);

    }

    if (loading) {
        return <p>Loading budgets...</p>;
    }

    if (error) {
        return <p>Failed to load budgets.</p>;
    }

    return (

        <MainLayout>

            <div className="flex justify-between items-center mb-8">

                <h1 className="text-3xl font-bold">
                    Budgets
                </h1>

                <button
                    onClick={() => {

                        setEditingBudget(null);
                        setShowForm(true);

                    }}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded-lg"
                >
                    + Add Budget
                </button>

            </div>

            {showForm && (

                <BudgetForm
                    budget={editingBudget}
                    onBudgetCreated={() => {

                        refetch();

                        setShowForm(false);

                    }}
                    onBudgetUpdated={() => {

                        refetch();

                        setEditingBudget(null);

                        setShowForm(false);

                    }}
                />

            )}

            {summary.length === 0 ? (

                <div className="text-center py-20 text-gray-500">

                    <p className="text-xl">
                        No budgets found.
                    </p>

                    <p className="mt-2">
                        Click <strong>+ Add Budget</strong> to create your first budget.
                    </p>

                </div>

            ) : (

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                    {summary.map((budget) => (

                        <BudgetCard
                            key={budget.id}
                            budget={budget}
                            onEdit={editBudget}
                            onDelete={removeBudget}
                        />

                    ))}

                </div>

            )}

        </MainLayout>

    );

}