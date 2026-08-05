import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import Goals from "./pages/Goals";
import Budget from "./pages/Budget";
import UploadStatement from "./pages/UploadStatement";

export default function App() {

    return (

        <Routes>

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
                element={<Dashboard />}
            />

            <Route
                path="/transactions"
                element={<Transactions />}
            />
            <Route
                path="/upload"
                element={<UploadStatement />}
            />
            <Route
                path="/goals"
                element={<Goals />}
            />
            <Route
                path="/budget"
                element={<Budget />}
            />

            <Route
                path="*"
                element={
                    <Navigate
                        to="/login"
                        replace
                    />
                }
            />

        </Routes>

    );

}