import api from "./axios";

export const getDailyPulse = (month, year) =>
    api
        .get("/ai/pulse", {
            params: {
                month,
                year,
            },
        })
        .then((res) => res.data);