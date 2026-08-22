import { Routes, Route, Navigate } from "react-router-dom";

import Login from "../pages/Login";
import Register from "../pages/Register";
import Dashboard from "../pages/Dashboard";
import Transactions from "../pages/Transactions";
import Budget from "../pages/Budget";
import Goals from "../pages/Goals";
import AI from "../pages/AI";
import UploadStatement from "../pages/UploadStatement";
import ProtectedRoute from "./ProtectedRoute";

export default function AppRoutes() {

    return (

        <Routes>

            <Route
                path="/"
                element={<Navigate to="/login" replace />}
            />

            <Route
                path="/login"
                element={<Login />}
            />

            <Route
                path="/register"
                element={<Register />}
            />

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
                path="*"
                element={<h1>404 Page Not Found</h1>}
            />

        </Routes>

    );

}