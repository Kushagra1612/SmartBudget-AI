import api from "./axios";

export const register = (data) =>
    api.post("/auth/register", data);

export const login = async (data) => {

    const formData = new URLSearchParams();

    formData.append("username", data.email);
    formData.append("password", data.password);

    return api.post(
        "/auth/login",
        formData,
        {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        }
    );
};

export const getProfile = () =>
    api.get("/auth/me");