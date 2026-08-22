import {
    House,
    Wallet,
    Target,
    ChartColumn,
    Bot,
    LogOut,
} from "lucide-react";

import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const items = [
    {
        icon: House,
        path: "/dashboard",
    },
    {
        icon: Wallet,
        path: "/transactions",
    },
    {
        icon: Target,
        path: "/goals",
    },
    {
        icon: ChartColumn,
        path: "/budget",
    },
    {
        icon: Bot,
        path: "/ai",
    },
];

export default function FloatingDock() {

    const navigate = useNavigate();
    const { setUser } = useAuth();

    const handleLogout = () => {

        localStorage.removeItem("access_token");
        localStorage.removeItem("token_type");

        setUser(null);

        navigate("/login");

    };

    return (

        <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50">

            <div
                className="
                    flex
                    items-center
                    gap-4
                    rounded-full
                    bg-white/80
                    backdrop-blur-xl
                    border
                    border-gray-200
                    px-5
                    py-3
                    shadow-[0_20px_60px_rgba(15,23,42,.15)]
                "
            >

                {items.map((item) => {

                    const Icon = item.icon;

                    return (

                        <NavLink
                            key={item.path}
                            to={item.path}
                            className={({ isActive }) =>
                                `
                                w-12
                                h-12
                                rounded-full
                                flex
                                items-center
                                justify-center
                                transition-all
                                duration-300
                                ${
                                    isActive
                                        ? "bg-[var(--primary)] text-white scale-110"
                                        : "text-gray-500 hover:bg-gray-100 hover:scale-105"
                                }
                            `
                            }
                        >
                            <Icon size={22} />
                        </NavLink>

                    );

                })}

                <div className="w-px h-8 bg-gray-200" />

                <button
                    type="button"
                    onClick={handleLogout}
                    title="Log out"
                    className="
                        w-12
                        h-12
                        rounded-full
                        flex
                        items-center
                        justify-center
                        text-gray-500
                        hover:bg-red-50
                        hover:text-red-500
                        hover:scale-105
                        transition-all
                        duration-300
                    "
                >
                    <LogOut size={22} />
                </button>

            </div>

        </div>

    );

}