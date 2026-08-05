import api from "./axios";

export async function getBudgets(month, year) {

    const response = await api.get("/budgets", {
        params: {
            month,
            year,
        },
    });

    return response.data;
}