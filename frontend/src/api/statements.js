import api from "./axios";

export const getStatements = () =>
    api.get("/statements").then((res) => res.data);

export const deleteStatement = (id) =>
    api.delete(`/statements/${id}`).then((res) => res.data);