import AuthLayout from "../components/layout/AuthLayout";
import LoginForm from "../components/auth/LoginForm";

export default function Login() {

    return (
        <AuthLayout title="Sign in to your account">

            <LoginForm />

        </AuthLayout>
    );

}