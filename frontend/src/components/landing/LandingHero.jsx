import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight, ShieldCheck, Brain } from "lucide-react";

import dashboardPreview from "../../assets/images/dashboard-preview.png";

export default function LandingHero() {

    return (

        <section className="relative min-h-screen flex items-center overflow-hidden pt-20 pb-16">

            {/* ── Background gradient orbs ── same visual language as
                AuthLayout: they drift slowly on an infinite loop, tinted
                by the theme variables so light/dark adapts for free. */}

            <motion.div
                animate={{ x: [0, 40, 0], y: [0, 30, 0] }}
                transition={{
                    duration: 18,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="
                    absolute -top-32 -left-32
                    w-[500px] h-[500px]
                    rounded-full opacity-20 blur-3xl
                    pointer-events-none
                "
                style={{ background: "var(--primary)" }}
            />

            <motion.div
                animate={{ x: [0, -30, 0], y: [0, -40, 0] }}
                transition={{
                    duration: 22,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="
                    absolute -bottom-32 -right-32
                    w-[500px] h-[500px]
                    rounded-full opacity-15 blur-3xl
                    pointer-events-none
                "
                style={{ background: "var(--accent)" }}
            />

            <motion.div
                animate={{ x: [0, 20, 0], y: [0, -20, 0] }}
                transition={{
                    duration: 15,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="
                    absolute top-1/3 right-1/4
                    w-[300px] h-[300px]
                    rounded-full opacity-10 blur-3xl
                    pointer-events-none
                "
                style={{ background: "var(--success)" }}
            />

            {/* ── Content grid ── */}

            <div className="
                relative z-10
                max-w-7xl mx-auto px-6 w-full
                grid grid-cols-1 lg:grid-cols-2
                gap-12 lg:gap-16 items-center
            ">

                {/* ── Left column: text ── */}

                <motion.div
                    initial={{ opacity: 0, x: -30 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6, ease: "easeOut" }}
                >

                    <span className="
                        inline-flex items-center gap-2
                        px-4 py-1.5 rounded-full
                        text-xs font-semibold
                        bg-indigo-100 text-indigo-700
                        dark:bg-indigo-500/20 dark:text-indigo-300
                    ">
                        <Brain size={14} />
                        AI-Powered Finance
                    </span>

                    <h1 className="
                        mt-6
                        text-4xl sm:text-5xl lg:text-6xl
                        font-extrabold tracking-tight
                        text-[var(--text)]
                    ">
                        SMARTBUDGET{" "}
                        <span className="text-[var(--primary)]">AI</span>
                    </h1>

                    <h2 className="
                        mt-3
                        text-xl sm:text-2xl
                        font-semibold
                        text-[var(--text-light)]
                    ">
                        Expense Manager App
                    </h2>

                    <p className="
                        mt-6
                        text-base sm:text-lg
                        text-[var(--text-light)]
                        max-w-lg leading-relaxed
                    ">
                        Manage your personal finances and easily track your
                        money, expenses, and budget — powered by AI insights,
                        anomaly detection, and smart recommendations.
                    </p>

                    <div className="mt-8 flex flex-wrap items-center gap-4">

                        {localStorage.getItem("access_token") ? (
                            <Link to="/dashboard">
                                <motion.button
                                    whileHover={{ scale: 1.03 }}
                                    whileTap={{ scale: 0.97 }}
                                    className="
                                        inline-flex items-center gap-2
                                        bg-[var(--primary)] text-white
                                        px-8 py-4 rounded-2xl
                                        font-semibold text-lg
                                        shadow-lg shadow-[var(--primary)]/25
                                        hover:brightness-110
                                        transition-all duration-300
                                    "
                                >
                                    Open Dashboard
                                    <ArrowRight size={20} />
                                </motion.button>
                            </Link>
                        ) : (
                            <>
                                <Link to="/register">
                                    <motion.button
                                        whileHover={{ scale: 1.03 }}
                                        whileTap={{ scale: 0.97 }}
                                        className="
                                            inline-flex items-center gap-2
                                            bg-[var(--primary)] text-white
                                            px-8 py-4 rounded-2xl
                                            font-semibold text-lg
                                            shadow-lg shadow-[var(--primary)]/25
                                            hover:brightness-110
                                            transition-all duration-300
                                        "
                                    >
                                        Get Started Free
                                        <ArrowRight size={20} />
                                    </motion.button>
                                </Link>

                                <Link
                                    to="/login"
                                    className="
                                        text-[var(--text-light)]
                                        hover:text-[var(--text)]
                                        font-medium transition-colors
                                        px-4 py-4
                                    "
                                >
                                    Log in →
                                </Link>
                            </>
                        )}

                    </div>

                </motion.div>

                {/* ── Right column: dashboard preview ── */}

                <motion.div
                    initial={{ opacity: 0, x: 30 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
                    className="relative"
                >

                    {/* Browser-chrome frame wrapping the real screenshot */}
                    <div className="
                        rounded-2xl overflow-hidden
                        shadow-2xl
                        border border-[var(--border)]
                        bg-[var(--surface)]
                    ">

                        {/* Fake browser top bar (3 dots + address bar) */}
                        <div className="
                            px-4 py-3
                            flex items-center gap-2
                            border-b border-[var(--border)]
                            bg-[var(--surface)]
                        ">
                            <div className="w-3 h-3 rounded-full bg-red-400" />
                            <div className="w-3 h-3 rounded-full bg-yellow-400" />
                            <div className="w-3 h-3 rounded-full bg-green-400" />

                            <div className="
                                flex-1 mx-4
                                bg-[var(--bg)] rounded-lg h-7
                                flex items-center px-3
                            ">
                                <span className="text-xs text-[var(--text-light)]">
                                    smartbudget.app/dashboard
                                </span>
                            </div>
                        </div>

                        {/* Actual dashboard screenshot */}
                        <img
                            src={dashboardPreview}
                            alt="SmartBudget AI Dashboard — Financial Health score, income, expenses, savings overview, and AI Daily Pulse"
                            className="w-full block"
                            loading="eager"
                        />

                    </div>

                    {/* ── Floating stat card: Financial Score ── */}

                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        transition={{ delay: 0.8, duration: 0.5 }}
                        className="
                            absolute -top-4 -right-4
                            sm:-top-6 sm:-right-6
                            hidden sm:block
                        "
                    >
                        <div className="
                            bg-[var(--surface)]/90
                            backdrop-blur-xl
                            border border-[var(--border)]
                            rounded-2xl px-4 py-3
                            shadow-lg
                            flex items-center gap-3
                        ">

                            <div className="
                                w-10 h-10 rounded-full
                                bg-green-100 dark:bg-green-500/20
                                flex items-center justify-center
                            ">
                                <ShieldCheck
                                    size={18}
                                    className="text-green-600 dark:text-green-400"
                                />
                            </div>

                            <div>
                                <p className="text-xs text-[var(--text-light)]">
                                    Financial Score
                                </p>
                                <p className="text-sm font-bold text-[var(--text)]">
                                    85 · Grade A
                                </p>
                            </div>

                        </div>
                    </motion.div>

                    {/* ── Floating stat card: AI Insights ── */}

                    <motion.div
                        initial={{ opacity: 0, y: 20, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        transition={{ delay: 1.1, duration: 0.5 }}
                        className="
                            absolute -bottom-4 -left-4
                            sm:-bottom-6 sm:-left-6
                            hidden sm:block
                        "
                    >
                        <div className="
                            bg-[var(--surface)]/90
                            backdrop-blur-xl
                            border border-[var(--border)]
                            rounded-2xl px-4 py-3
                            shadow-lg
                            flex items-center gap-3
                        ">

                            <div className="
                                w-10 h-10 rounded-full
                                bg-indigo-100 dark:bg-indigo-500/20
                                flex items-center justify-center
                            ">
                                <Brain
                                    size={18}
                                    className="text-indigo-600 dark:text-indigo-400"
                                />
                            </div>

                            <div>
                                <p className="text-xs text-[var(--text-light)]">
                                    AI Daily Pulse
                                </p>
                                <p className="text-sm font-bold text-[var(--success)]">
                                    Finances on Solid Ground
                                </p>
                            </div>

                        </div>
                    </motion.div>

                </motion.div>

            </div>

        </section>

    );

}
