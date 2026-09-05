import api from "./axios";

export const getGoals = () =>
    api.get("/goals").then((res) => res.data);

export const createGoal = (goal) =>
    api.post("/goals", goal).then((res) => res.data);

export const updateGoal = (id, goal) =>
    api.put(`/goals/${id}`, goal).then((res) => res.data);

export const contributeToGoal = (id, amount) =>
    api.post(`/goals/${id}/contribute`, { amount }).then((res) => res.data);

export const deleteGoal = (id) =>
    api.delete(`/goals/${id}`).then((res) => res.data);