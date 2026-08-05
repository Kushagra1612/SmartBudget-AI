import api from "./axios";

export async function getDashboard(month, year) {

    const response = await api.get("/dashboard", {
        params: {
            month,
            year,
        },
    });

    return response.data;
}