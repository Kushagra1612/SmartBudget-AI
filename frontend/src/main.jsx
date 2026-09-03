import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Toaster } from "react-hot-toast";

import AppRoutes from "./routes/AppRoutes";
import ErrorBoundary from "./components/common/ErrorBoundary";

import "./styles/globals.css";

import { AuthProvider } from "./context/AuthContext";

ReactDOM.createRoot(
    document.getElementById("root")
).render(

    <React.StrictMode>

        <ErrorBoundary>

            <Toaster
                position="top-right"
                toastOptions={{
                    duration: 4000,
                    style: {
                        background: "var(--surface)",
                        color: "var(--text)",
                        borderRadius: "16px",
                        boxShadow: "var(--shadow)",
                        padding: "14px 18px",
                        fontSize: "14px",
                    },
                    success: {
                        iconTheme: {
                            primary: "var(--success)",
                            secondary: "#fff",
                        },
                    },
                    error: {
                        iconTheme: {
                            primary: "var(--danger)",
                            secondary: "#fff",
                        },
                    },
                }}
            />

            <BrowserRouter>

                <AuthProvider>

                    <AppRoutes />

                </AuthProvider>

            </BrowserRouter>

        </ErrorBoundary>

    </React.StrictMode>

);