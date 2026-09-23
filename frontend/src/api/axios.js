import axios from "axios";

     const api = axios.create({
        baseURL: "https://smartbudgetai-m5ys.onrender.com",
     });

    //  const api = axios.create({
    //    baseURL: "http://localhost:8000",
    // });

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

api.interceptors.response.use(
    (response) => response,

    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("token_type");

            const publicPaths = ["/", "/login", "/register"];
            if (!publicPaths.includes(window.location.pathname)) {
                window.location.href = "/login";
            }
        }

        return Promise.reject(error);
    }
);

export default api;