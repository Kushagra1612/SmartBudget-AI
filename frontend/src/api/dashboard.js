import api from "./axios";

export const getDashboard = (month, year) =>
    api.get(`/dashboard?month=${month}&year=${year}`);