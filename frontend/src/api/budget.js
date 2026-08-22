import api from "./axios";

export const getBudgets = () =>
    api.get("/budgets").then((res) => res.data);

export const createBudget = (budget) =>
    api.post("/budgets", budget).then((res) => res.data);

export const updateBudget = (id, budget) =>
    api.put(`/budgets/${id}`, budget).then((res) => res.data);

export const deleteBudget = (id) =>
    api.delete(`/budgets/${id}`).then((res) => res.data);

export const getBudgetSummary = () =>
    api.get("/budgets/summary").then((res) => res.data);