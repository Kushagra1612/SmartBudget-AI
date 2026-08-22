import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Mail, Lock } from "lucide-react";
import { login, getProfile } from "../../api/auth";
import { useAuth } from "../../context/AuthContext";
import Button from "../common/Button";
import Input from "../common/Input";

export default function LoginForm() {

    const navigate = useNavigate();
    const { setUser } = useAuth();

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

            try {

                const profile = await getProfile();

                setUser(profile.data);

            } catch {

                // Non-fatal -- login itself already succeeded, and
                // AuthContext will retry fetching the profile the next
                // time the app mounts.

            }

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

            <Input
                type="email"
                name="email"
                placeholder="Email"
                value={form.email}
                onChange={handleChange}
                icon={Mail}
                required
            />

            <Input
                type="password"
                name="password"
                placeholder="Password"
                value={form.password}
                onChange={handleChange}
                icon={Lock}
                required
            />

            <Button
                type="submit"
                disabled={loading}
                className="w-full"
            >
                {loading ? "Signing In..." : "Login"}
            </Button>

        </form>

    );

}