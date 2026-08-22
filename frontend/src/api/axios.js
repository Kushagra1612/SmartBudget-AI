import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.request.use((config) => {

    const token = localStorage.getItem("access_token");

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

// A 401 means the token is missing, expired, or invalid -- the backend
// rejected it regardless of which. Clear it and send the user back to
// login instead of leaving every page stuck on a silent "Error loading..."
// state with no way back in.
api.interceptors.response.use(
    (response) => response,

    (error) => {

        if (error.response?.status === 401) {

            localStorage.removeItem("access_token");
            localStorage.removeItem("token_type");

            if (window.location.pathname !== "/login") {
                window.location.href = "/login";
            }

        }

        return Promise.reject(error);

    }
);

export default api;