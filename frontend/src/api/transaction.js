import api from "./axios";

export const getTransactions = () =>
    api.get("/transactions").then((res) => res.data);

export const updateTransaction = (id, updates) =>
    api.patch(`/transactions/${id}`, updates).then((res) => res.data);