import api from "./axios";

export const chat = (message, month, year) =>
    api.post("/ai/chat", {
        message,
        month,
        year,
    });

export const getAdvice = (month, year) =>
    api.post("/ai/advice", {
        month,
        year,
    });