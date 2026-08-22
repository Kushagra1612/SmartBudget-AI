import api from "./axios";

export const chat = async (message) => {

    const response = await api.post("/ai/chat", {
        message,
    });

    return response.data;

};

export const getAdvice = async () => {

    const response = await api.post("/ai/advice", {});

    return response.data;

};

export const getPulse = async () => {

    const response = await api.get("/ai/pulse");

    return response.data;

};