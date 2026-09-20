import { useState } from "react";
import { NavLink, useNavigate, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
    House,
    Wallet,
    Target,
    ChartColumn,
    Bot,
    Files,
    LogOut,
    Sun,
    Moon,
    Menu,
    X,
    ChevronRight,
} from "lucide-react";

import { useAuth } from "../../context/AuthContext";
import { useTheme } from "../../context/ThemeContext";

const navItems = [
    {
        name: "Dashboard",
        icon: House,
        path: "/dashboard",
    },
    {
        name: "Transactions",
        icon: Wallet,
        path: "/transactions",
    },
    {
        name: "Budgets",
        icon: ChartColumn,
        path: "/budget",
    },
    {
        name: "Goals",
        icon: Target,
        path: "/goals",
    },
    {
        name: "AI Assistant",
        icon: Bot,
        path: "/ai",
        badge: "AI",
    },
    {
        name: "Statements",
        icon: Files,
        path: "/statements",
    },
];

export default function Sidebar() {
    const { user, setUser } = useAuth();
    const { theme, toggleTheme } = useTheme();
    const navigate = useNavigate();
    const location = useLocation();
    const [mobileOpen, setMobileOpen] = useState(false);

    const handleLogout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("token_type");
        setUser(null);
        navigate("/");
    };

    const userInitial = (user?.full_name?.[0] || user?.email?.[0] || "U").toUpperCase();
    const displayName = user?.full_name || user?.email?.split("@")[0] || "User";

    const sidebarContent = (
        <div className="h-full flex flex-col justify-between p-5 bg-[var(--surface)] select-none">
            {/* Top: Logo and Brand */}
            <div>
                <div className="flex items-center justify-between pb-6 border-b border-[var(--border)]">
                    <NavLink to="/dashboard" className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-2xl bg-[var(--primary)] flex items-center justify-center text-white shadow-md shadow-[var(--primary)]/30">
                            <Wallet size={20} />
                        </div>
                        <div>
                            <span className="font-extrabold text-base tracking-tight text-[var(--text)] block leading-tight">
                                SmartBudget <span className="text-[var(--primary)]">AI</span>
                            </span>
                            <span className="text-[11px] font-medium text-[var(--text-light)]">
                                Finance Assistant
                            </span>
                        </div>
                    </NavLink>

                    {/* Mobile close button */}
                    <button
                        type="button"
                        onClick={() => setMobileOpen(false)}
                        className="lg:hidden p-1.5 rounded-xl text-[var(--text-light)] hover:bg-[var(--bg)]"
                    >
                        <X size={20} />
                    </button>
                </div>

                {/* Navigation Links */}
                <nav className="mt-6 space-y-1.5">
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        const isActive = location.pathname === item.path;

                        return (
                            <NavLink
                                key={item.path}
                                to={item.path}
                                onClick={() => setMobileOpen(false)}
                                className={`
                                    relative flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200
                                    ${
                                        isActive
                                            ? "bg-[var(--primary)] text-white shadow-md shadow-[var(--primary)]/25"
                                            : "text-[var(--text-light)] hover:text-[var(--text)] hover:bg-[var(--bg)]"
                                    }
                                `}
                            >
                                <div className="flex items-center gap-3">
                                    <Icon size={19} className={isActive ? "text-white" : "text-[var(--text-light)]"} />
                                    <span>{item.name}</span>
                                </div>

                                {item.badge && (
                                    <span
                                        className={`
                                            px-2 py-0.5 rounded-full text-[10px] font-bold tracking-wide uppercase
                                            ${
                                                isActive
                                                    ? "bg-white/20 text-white"
                                                    : "bg-indigo-100 text-indigo-700 dark:bg-indigo-500/20 dark:text-indigo-300"
                                            }
                                        `}
                                    >
                                        {item.badge}
                                    </span>
                                )}
                            </NavLink>
                        );
                    })}
                </nav>
            </div>

            {/* Bottom: User Card, Theme Toggle & Logout */}
            <div className="pt-4 border-t border-[var(--border)] space-y-3">
                {/* User Info Card (Clickable to /profile) */}
                <NavLink
                    to="/profile"
                    onClick={() => setMobileOpen(false)}
                    title="View Account Profile & Settings"
                    className={({ isActive }) => `
                        flex items-center justify-between p-2.5 rounded-2xl transition-all duration-200 group
                        ${
                            isActive
                                ? "bg-[var(--primary)]/10 border-[var(--primary)] text-[var(--primary)] shadow-sm"
                                : "bg-[var(--bg)] hover:bg-[var(--border)]/30 border-[var(--border)] hover:border-[var(--primary)]/40"
                        }
                        border
                    `}
                >
                    <div className="flex items-center gap-3 min-w-0">
                        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-[var(--primary)] to-[var(--accent)] text-white flex items-center justify-center font-bold text-sm shrink-0 shadow-sm">
                            {userInitial}
                        </div>
                        <div className="min-w-0 text-left">
                            <p className="text-xs font-bold text-[var(--text)] truncate group-hover:text-[var(--primary)] transition-colors">
                                {displayName}
                            </p>
                            <p className="text-[11px] text-[var(--text-light)] truncate">
                                {user?.email || "Account & Settings"}
                            </p>
                        </div>
                    </div>
                    <ChevronRight size={15} className="text-[var(--text-light)] group-hover:text-[var(--primary)] group-hover:translate-x-0.5 transition-all shrink-0 ml-1" />
                </NavLink>

                {/* Bottom Actions: Theme Switcher & Logout */}
                <div className="flex items-center gap-2">
                    <button
                        type="button"
                        onClick={toggleTheme}
                        title={theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode"}
                        className="
                            flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xl
                            text-xs font-semibold
                            bg-[var(--bg)] text-[var(--text-light)] hover:text-[var(--text)]
                            border border-[var(--border)] hover:border-[var(--text-light)]/30
                            transition-all duration-200
                        "
                    >
                        {theme === "dark" ? (
                            <>
                                <Sun size={15} className="text-amber-400" />
                                <span>Light</span>
                            </>
                        ) : (
                            <>
                                <Moon size={15} className="text-indigo-500" />
                                <span>Dark</span>
                            </>
                        )}
                    </button>

                    <button
                        type="button"
                        onClick={handleLogout}
                        title="Sign out"
                        className="
                            flex items-center justify-center p-2 rounded-xl
                            text-xs font-semibold text-[var(--text-light)] hover:text-red-500
                            bg-[var(--bg)] hover:bg-red-50 dark:hover:bg-red-950/30
                            border border-[var(--border)] hover:border-red-300 dark:hover:border-red-900
                            transition-all duration-200
                        "
                    >
                        <LogOut size={16} />
                    </button>
                </div>
            </div>
        </div>
    );

    return (
        <>
            {/* Desktop Fixed Sidebar */}
            <aside className="hidden lg:block fixed inset-y-0 left-0 w-64 border-r border-[var(--border)] z-30 shadow-sm">
                {sidebarContent}
            </aside>

            {/* Mobile Header Bar */}
            <header className="lg:hidden fixed top-0 left-0 right-0 h-16 bg-[var(--surface)]/90 backdrop-blur-md border-b border-[var(--border)] z-40 px-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-xl bg-[var(--primary)] flex items-center justify-center text-white">
                        <Wallet size={16} />
                    </div>
                    <span className="font-bold text-sm text-[var(--text)]">
                        SmartBudget AI
                    </span>
                </div>

                <div className="flex items-center gap-2">
                    <button
                        type="button"
                        onClick={toggleTheme}
                        className="p-2 rounded-xl text-[var(--text-light)] hover:bg-[var(--bg)]"
                    >
                        {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
                    </button>
                    <button
                        type="button"
                        onClick={() => setMobileOpen(true)}
                        className="p-2 rounded-xl text-[var(--text-light)] hover:bg-[var(--bg)]"
                    >
                        <Menu size={20} />
                    </button>
                </div>
            </header>

            {/* Mobile Drawer Overlay */}
            <AnimatePresence>
                {mobileOpen && (
                    <>
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setMobileOpen(false)}
                            className="lg:hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
                        />
                        <motion.aside
                            initial={{ x: "-100%" }}
                            animate={{ x: 0 }}
                            exit={{ x: "-100%" }}
                            transition={{ type: "spring", damping: 25, stiffness: 280 }}
                            className="lg:hidden fixed inset-y-0 left-0 w-72 max-w-[80vw] z-50 shadow-2xl border-r border-[var(--border)]"
                        >
                            {sidebarContent}
                        </motion.aside>
                    </>
                )}
            </AnimatePresence>
        </>
    );
}
