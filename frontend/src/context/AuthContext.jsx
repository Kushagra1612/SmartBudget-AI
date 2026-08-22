import { createContext, useContext, useEffect, useState } from "react";
import { getProfile } from "../api/auth";

const AuthContext = createContext();

export function AuthProvider({ children }) {

    const [user, setUser] = useState(null);

    // Populated once on mount, and again from LoginForm right after a
    // fresh login. Covers both cases: a brand new session, and a page
    // refresh where only the token (not the user) survived in memory.
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        const token = localStorage.getItem("access_token");

        if (!token) {
            setLoading(false);
            return;
        }

        getProfile()
            .then((response) => {
                setUser(response.data);
            })
            .catch(() => {
                // Invalid/expired token. The axios response interceptor
                // already clears storage and redirects to /login on a
                // 401, so there's nothing extra to do here.
            })
            .finally(() => {
                setLoading(false);
            });

    }, []);

    return (
        <AuthContext.Provider
            value={{
                user,
                setUser,
                loading,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}