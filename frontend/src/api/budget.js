import api from "./axios";

export const getBudgets = (month, year) =>
    api.get("/budgets", {
        params: {
            month,
            year,
        },
    }).then((res) => res.data);

export const createBudget = (budget) =>
    api.post("/budgets", budget).then((res) => res.data);

export const updateBudget = (id, budget) =>
    api.put(`/budgets/${id}`, budget).then((res) => res.data);

export const deleteBudget = (id) =>
    api.delete(`/budgets/${id}`).then((res) => res.data);

export const getBudgetSummary = (month, year) =>
    api.get("/budgets/summary", {
        params: {
            month,
            year,
        },
    }).then((res) => res.data);