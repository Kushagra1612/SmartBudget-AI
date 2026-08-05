import api from "./axios";

export const getTransactions = () =>
    api.get("/transactions").then((res) => res.data);