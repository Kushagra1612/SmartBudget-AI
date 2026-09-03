import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { User, Mail, Lock } from "lucide-react";
import toast from "react-hot-toast";
import { register } from "../../api/auth";
import Button from "../common/Button";
import Input from "../common/Input";

export default function RegisterForm() {

    const navigate = useNavigate();

    const [form, setForm] = useState({
        full_name: "",
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

            await register(form);

            toast.success("Registration successful!");

            navigate("/login");

        } catch (error) {

            toast.error(
                error.response?.data?.detail ??
                "Registration failed"
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
                name="full_name"
                placeholder="Full Name"
                value={form.full_name}
                onChange={handleChange}
                icon={User}
                required
            />

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
                {loading ? "Creating..." : "Create Account"}
            </Button>

        </form>

    );

}