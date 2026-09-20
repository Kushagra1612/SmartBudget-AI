import React, { Suspense, lazy } from "react";
import { Routes, Route } from "react-router-dom";

import LandingPage from "../pages/LandingPage";
import Login from "../pages/Login";
import Register from "../pages/Register";
import ProtectedRoute from "./ProtectedRoute";

// Code splitting: lazy-load authenticated pages so the initial landing page bundle remains lightweight
const Dashboard = lazy(() => import("../pages/Dashboard"));
const Transactions = lazy(() => import("../pages/Transactions"));
const Budget = lazy(() => import("../pages/Budget"));
const Goals = lazy(() => import("../pages/Goals"));
const AI = lazy(() => import("../pages/AI"));
const UploadStatement = lazy(() => import("../pages/UploadStatement"));
const Statements = lazy(() => import("../pages/Statements"));
const Profile = lazy(() => import("../pages/Profile"));

function PageFallback() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-[var(--bg)]">
            <div className="w-9 h-9 border-3 border-[var(--border)] border-t-[var(--primary)] rounded-full animate-spin" />
        </div>
    );
}

export default function AppRoutes() {
    return (
        <Suspense fallback={<PageFallback />}>
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/transactions"
                    element={
                        <ProtectedRoute>
                            <Transactions />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/budget"
                    element={
                        <ProtectedRoute>
                            <Budget />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/goals"
                    element={
                        <ProtectedRoute>
                            <Goals />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/ai"
                    element={
                        <ProtectedRoute>
                            <AI />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/upload"
                    element={
                        <ProtectedRoute>
                            <UploadStatement />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/statements"
                    element={
                        <ProtectedRoute>
                            <Statements />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/profile"
                    element={
                        <ProtectedRoute>
                            <Profile />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="*"
                    element={
                        <div className="min-h-screen flex flex-col items-center justify-center bg-[var(--bg)] text-[var(--text)]">
                            <h1 className="text-3xl font-bold">404 Page Not Found</h1>
                            <p className="mt-2 text-[var(--text-light)]">The page you are looking for does not exist.</p>
                        </div>
                    }
                />
            </Routes>
        </Suspense>
    );
}