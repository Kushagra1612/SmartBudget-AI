import { Link, Navigate } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout";
import LoginForm from "../components/auth/LoginForm";

export default function Login() {

    const token = localStorage.getItem("access_token");

    if (token) {
        return <Navigate to="/dashboard" replace />;
    }

    return (
        <AuthLayout title="Sign in to your account">

            <LoginForm />

            <p className="text-center text-sm text-[var(--text-light)] mt-6">
                Don't have an account?{" "}
                <Link
                    to="/register"
                    className="text-blue-600 font-medium hover:underline"
                >
                    Sign up
                </Link>
            </p>

        </AuthLayout>
    );

}