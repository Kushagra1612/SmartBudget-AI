import api from "./axios";

export const getGoals = () =>
    api.get("/goals");

export const createGoal = (goal) =>
    api.post("/goals", goal);

export const updateGoal = (id, goal) =>
    api.put(`/goals/${id}`, goal);

export const deleteGoal = (id) =>
    api.delete(`/goals/${id}`);