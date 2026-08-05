import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../../api/auth";

export default function LoginForm() {

    const navigate = useNavigate();

    const [form, setForm] = useState({
        email: "",
        password: "",
    });

    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {

        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        try {

            setLoading(true);

            const response = await login(form);

            localStorage.removeItem("access_token");
            localStorage.removeItem("token_type"); 
            
            localStorage.setItem(
                "access_token",
                response.data.access_token
            );

            localStorage.setItem(
                "token_type",
                response.data.token_type
            );

            navigate("/dashboard");

        } catch (error) {

            alert(
                error.response?.data?.detail ??
                "Login failed"
            );

        } finally {

            setLoading(false);

        }

    };

    return (

        <form
            onSubmit={handleSubmit}
            className="space-y-4"
        >

            <input
                type="email"
                name="email"
                placeholder="Email"
                value={form.email}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            <input
                type="password"
                name="password"
                placeholder="Password"
                value={form.password}
                onChange={handleChange}
                className="w-full border rounded-lg p-3"
                required
            />

            <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white rounded-lg p-3"
            >
                {loading ? "Signing In..." : "Login"}
            </button>

        </form>

    );

}