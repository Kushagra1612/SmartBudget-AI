import { useEffect, useState } from "react";

import MainLayout from "../layouts/MainLayout";
import BudgetForm from "../components/budget/BudgetForm";
import BudgetCard from "../components/budget/BudgetCard";
import useBudgetSummary from "../hooks/useBudgetSummary";

export default function Budget() {

    const {
        summary,
        loading,
        error,
    } = useBudgetSummary();

    const [budgetList, setBudgetList] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [editingBudget, setEditingBudget] = useState(null);

    useEffect(() => {

        setBudgetList(summary);

    }, [summary]);

    function addBudget(budget) {

        setBudgetList((prev) => [
            budget,
            ...prev,
        ]);

    }

    function removeBudget(id) {

        setBudgetList((prev) =>
            prev.filter((budget) => budget.id !== id)
        );
        setEditingBudget(null);
        setShowForm(false);


    }

    function editBudget(budget) {

        setEditingBudget(budget);
        setShowForm(true);

    }

    function updateExistingBudget(updatedBudget) {

        setBudgetList((prev) =>
            prev.map((budget) =>
                budget.id === updatedBudget.id
                    ? {
                          ...budget,
                          monthly_limit: updatedBudget.monthly_limit,
                      }
                    : budget
            )
        );

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
                    onBudgetCreated={(budget) => {

                        addBudget(budget);

                        setShowForm(false);

                        window.location.reload();

                    }}
                    onBudgetUpdated={(budget) => {

                        updateExistingBudget(budget);

                        setEditingBudget(null);

                        setShowForm(false);

                    }}
                />

            )}

            {budgetList.length === 0 ? (

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

                    {budgetList.map((budget) => (

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