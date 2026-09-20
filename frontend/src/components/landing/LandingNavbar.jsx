import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Wallet, Sun, Moon } from "lucide-react";
import { useTheme } from "../../context/ThemeContext";

export default function LandingNavbar() {

    const { theme, toggleTheme } = useTheme();

    return (

        <motion.nav
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="
                fixed top-0 left-0 right-0 z-50
                bg-[var(--bg)]/80
                backdrop-blur-xl
                border-b border-[var(--border)]
            "
        >

            <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">

                {/* Logo */}
                <Link
                    to="/"
                    className="flex items-center gap-3"
                >

                    <div
                        className="
                            w-10 h-10 rounded-xl
                            bg-[var(--primary)]
                            flex items-center justify-center
                        "
                    >
                        <Wallet size={20} className="text-white" />
                    </div>

                    <span className="text-lg font-bold text-[var(--text)]">
                        SmartBudget AI
                    </span>

                </Link>

                {/* Center nav links — hidden on small screens */}
                <div className="hidden md:flex items-center gap-8">

                    <a
                        href="#features"
                        className="
                            text-sm font-medium
                            text-[var(--text-light)]
                            hover:text-[var(--text)]
                            transition-colors
                        "
                    >
                        Features
                    </a>

                </div>

                {/* Right-side actions */}
                <div className="flex items-center gap-3">

                    {/* Inline theme toggle — NOT the fixed-position
                        ThemeToggleButton component, so it sits inside
                        the nav flow instead of floating over content. */}
                    <button
                        type="button"
                        onClick={toggleTheme}
                        title={
                            theme === "dark"
                                ? "Switch to light mode"
                                : "Switch to dark mode"
                        }
                        className="
                            w-10 h-10 rounded-full
                            flex items-center justify-center
                            text-[var(--text-light)]
                            hover:text-[var(--text)]
                            hover:bg-[var(--surface)]
                            transition-all duration-300
                        "
                    >
                        {theme === "dark"
                            ? <Sun size={18} />
                            : <Moon size={18} />
                        }
                    </button>

                    {localStorage.getItem("access_token") ? (
                        <Link
                            to="/dashboard"
                            className="
                                text-sm font-semibold
                                bg-[var(--primary)] text-white
                                px-5 py-2.5 rounded-xl
                                hover:brightness-110
                                transition-all
                            "
                        >
                            Open Dashboard →
                        </Link>
                    ) : (
                        <>
                            <Link
                                to="/login"
                                className="
                                    text-sm font-medium
                                    text-[var(--text-light)]
                                    hover:text-[var(--text)]
                                    transition-colors
                                    px-4 py-2
                                "
                            >
                                Log in
                            </Link>

                            <Link
                                to="/register"
                                className="
                                    text-sm font-semibold
                                    bg-[var(--primary)] text-white
                                    px-5 py-2.5 rounded-xl
                                    hover:brightness-110
                                    transition-all
                                "
                            >
                                Get Started
                            </Link>
                        </>
                    )}

                </div>

            </div>

        </motion.nav>

    );

}
