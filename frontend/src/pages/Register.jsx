import { Link } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout";
import RegisterForm from "../components/auth/RegisterForm";

export default function Register() {

    return (

        <AuthLayout title="Create your account">

            <RegisterForm />

            <p className="text-center text-sm text-gray-500 mt-6">
                Already have an account?{" "}
                <Link
                    to="/login"
                    className="text-blue-600 font-medium hover:underline"
                >
                    Sign in
                </Link>
            </p>

        </AuthLayout>

    );

}