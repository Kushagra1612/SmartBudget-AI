import api from "./axios";

export const uploadStatement = async (file) => {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/upload/statement",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;

};