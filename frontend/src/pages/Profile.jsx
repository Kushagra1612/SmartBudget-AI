import {
    Mail,
    Shield,
    Coins,
    Sparkles,
    Sun,
    Moon,
    LogOut,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";
import Card from "../components/common/Card";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";
import useDashboard from "../hooks/useDashboard";
import useStatements from "../hooks/useStatements";

export default function Profile() {
    const { user, setUser } = useAuth();
    const { theme, toggleTheme } = useTheme();
    const navigate = useNavigate();

    const { dashboard } = useDashboard();
    const { statements } = useStatements();

    const handleLogout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("token_type");
        setUser(null);
        navigate("/");
    };

    const userInitial = (user?.full_name?.[0] || user?.email?.[0] || "U").toUpperCase();
    const displayName = user?.full_name || "User";

    return (
        <MainLayout>
            <div className="max-w-4xl mx-auto py-2">
                {/* Page Title */}
                <div className="mb-8">
                    <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-[var(--text)]">
                        Account & Profile
                    </h1>
                    <p className="mt-1 text-sm text-[var(--text-light)]">
                        Manage your personal profile, financial preferences, and account security.
                    </p>
                </div>

                <div className="space-y-6">
                    {/* Main Identity Card */}
                    <Card hover={false} className="p-6 sm:p-8">
                        <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6">
                            <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-[var(--primary)] to-[var(--accent)] text-white flex items-center justify-center font-extrabold text-3xl shadow-lg shadow-[var(--primary)]/30 shrink-0">
                                {userInitial}
                            </div>

                            <div className="flex-1 text-center sm:text-left min-w-0">
                                <div className="flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
                                    <div>
                                        <h2 className="text-2xl font-bold text-[var(--text)] truncate">
                                            {displayName}
                                        </h2>
                                        <p className="text-sm text-[var(--text-light)] flex items-center justify-center sm:justify-start gap-1.5 mt-1">
                                            <Mail size={15} />
                                            <span>{user?.email}</span>
                                        </p>
                                    </div>

                                    <span className="self-center sm:self-start inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-300">
                                        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                                        Active Account
                                    </span>
                                </div>

                                <div className="mt-6 pt-6 border-t border-[var(--border)] grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
                                    <div className="p-3 rounded-2xl bg-[var(--bg)] border border-[var(--border)]">
                                        <p className="text-xs text-[var(--text-light)]">Statements</p>
                                        <p className="text-xl font-extrabold text-[var(--text)] mt-0.5">
                                            {statements?.length || 0}
                                        </p>
                                    </div>

                                    <div className="p-3 rounded-2xl bg-[var(--bg)] border border-[var(--border)]">
                                        <p className="text-xs text-[var(--text-light)]">Health Score</p>
                                        <p className="text-xl font-extrabold text-[var(--success)] mt-0.5">
                                            {dashboard?.analytics?.financial_score?.score ?? "—"}
                                            <span className="text-xs font-normal text-[var(--text-light)] ml-1">/ 100</span>
                                        </p>
                                    </div>

                                    <div className="p-3 rounded-2xl bg-[var(--bg)] border border-[var(--border)]">
                                        <p className="text-xs text-[var(--text-light)]">Base Currency</p>
                                        <p className="text-xl font-extrabold text-[var(--text)] mt-0.5">
                                            ₹ INR
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </Card>

                    {/* Preferences & System Settings */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Financial Preferences Card */}
                        <Card hover={false} className="p-6">
                            <div className="flex items-center gap-3 mb-5">
                                <div className="w-9 h-9 rounded-xl bg-indigo-100 dark:bg-indigo-500/20 text-[var(--primary)] flex items-center justify-center">
                                    <Coins size={18} />
                                </div>
                                <div>
                                    <h3 className="font-bold text-[var(--text)] text-base">
                                        Financial Defaults
                                    </h3>
                                    <p className="text-xs text-[var(--text-light)]">
                                        Currency and formatting rules
                                    </p>
                                </div>
                            </div>

                            <div className="space-y-3">
                                <div className="flex items-center justify-between p-3 rounded-xl bg-[var(--bg)] border border-[var(--border)]">
                                    <div>
                                        <p className="text-xs font-semibold text-[var(--text)]">Default Currency</p>
                                        <p className="text-[11px] text-[var(--text-light)]">Indian Rupee (Lakhs / Crores)</p>
                                    </div>
                                    <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-[var(--surface)] text-[var(--primary)] border border-[var(--border)]">
                                        ₹ INR
                                    </span>
                                </div>

                                <div className="flex items-center justify-between p-3 rounded-xl bg-[var(--bg)] border border-[var(--border)]">
                                    <div>
                                        <p className="text-xs font-semibold text-[var(--text)]">AI Engine</p>
                                        <p className="text-[11px] text-[var(--text-light)]">LangGraph 4-Agent Pipeline</p>
                                    </div>
                                    <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-bold bg-purple-100 dark:bg-purple-500/20 text-purple-700 dark:text-purple-300">
                                        <Sparkles size={12} />
                                        Gemini
                                    </span>
                                </div>
                            </div>
                        </Card>

                        {/* Theme & Display Card */}
                        <Card hover={false} className="p-6">
                            <div className="flex items-center gap-3 mb-5">
                                <div className="w-9 h-9 rounded-xl bg-amber-100 dark:bg-amber-500/20 text-amber-600 dark:text-amber-400 flex items-center justify-center">
                                    {theme === "dark" ? <Moon size={18} /> : <Sun size={18} />}
                                </div>
                                <div>
                                    <h3 className="font-bold text-[var(--text)] text-base">
                                        Theme & Interface
                                    </h3>
                                    <p className="text-xs text-[var(--text-light)]">
                                        Choose your visual experience
                                    </p>
                                </div>
                            </div>

                            <div className="p-3 rounded-xl bg-[var(--bg)] border border-[var(--border)] flex items-center justify-between">
                                <div>
                                    <p className="text-xs font-semibold text-[var(--text)]">Interface Mode</p>
                                    <p className="text-[11px] text-[var(--text-light)]">Currently: {theme === "dark" ? "Dark Mode" : "Light Mode"}</p>
                                </div>

                                <button
                                    type="button"
                                    onClick={toggleTheme}
                                    className="px-4 py-2 rounded-xl text-xs font-semibold bg-[var(--surface)] hover:bg-[var(--border)]/50 text-[var(--text)] border border-[var(--border)] flex items-center gap-2 transition-all"
                                >
                                    {theme === "dark" ? (
                                        <>
                                            <Sun size={14} className="text-amber-400" />
                                            <span>Switch to Light</span>
                                        </>
                                    ) : (
                                        <>
                                            <Moon size={14} className="text-indigo-500" />
                                            <span>Switch to Dark</span>
                                        </>
                                    )}
                                </button>
                            </div>
                        </Card>
                    </div>

                    {/* Account Security & Sign Out Card */}
                    <Card hover={false} className="p-6">
                        <div className="flex items-center gap-3 mb-5">
                            <div className="w-9 h-9 rounded-xl bg-rose-100 dark:bg-rose-500/20 text-rose-600 dark:text-rose-400 flex items-center justify-center">
                                <Shield size={18} />
                            </div>
                            <div>
                                <h3 className="font-bold text-[var(--text)] text-base">
                                    Security & Session
                                </h3>
                                <p className="text-xs text-[var(--text-light)]">
                                    Manage your credentials and session state
                                </p>
                            </div>
                        </div>

                        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl bg-[var(--bg)] border border-[var(--border)]">
                            <div>
                                <p className="text-sm font-semibold text-[var(--text)]">Signed in as {user?.email}</p>
                                <p className="text-xs text-[var(--text-light)] mt-0.5">
                                    JWT authenticated session with encrypted password storage.
                                </p>
                            </div>

                            <div className="flex items-center gap-3 w-full sm:w-auto">
                                <button
                                    type="button"
                                    onClick={handleLogout}
                                    className="
                                        w-full sm:w-auto px-5 py-2.5 rounded-xl
                                        text-xs font-bold
                                        text-red-600 hover:text-white
                                        bg-red-50 hover:bg-red-600 dark:bg-red-950/30 dark:hover:bg-red-600
                                        border border-red-200 dark:border-red-900
                                        flex items-center justify-center gap-2
                                        transition-all duration-200
                                    "
                                >
                                    <LogOut size={15} />
                                    <span>Log out</span>
                                </button>
                            </div>
                        </div>
                    </Card>
                </div>
            </div>
        </MainLayout>
    );
}
