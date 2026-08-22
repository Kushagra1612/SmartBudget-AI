import api from "./axios";

export async function getAnomalies() {

    const response = await api.get("/anomalies");

    return response.data;

}
