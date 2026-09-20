import { motion } from "framer-motion";
import { Wallet } from "lucide-react";
import ThemeToggleButton from "../components/common/ThemeToggleButton";

export default function AuthLayout({ title, children }) {
    return (
        <div className="relative min-h-screen bg-[var(--bg)] flex items-center justify-center overflow-hidden">

            <ThemeToggleButton />

            {/* Soft blurred gradient orbs -- purely decorative, sit
                behind the form card (z-index below it). Colors come
                from the existing theme variables so this adapts to
                light/dark mode automatically instead of needing a
                separate treatment per theme. */}
            <motion.div
                animate={{
                    x: [0, 40, 0],
                    y: [0, 30, 0],
                }}
                transition={{
                    duration: 18,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="absolute -top-32 -left-32 w-[420px] h-[420px] rounded-full opacity-30 blur-3xl"
                style={{ background: "var(--primary)" }}
            />

            <motion.div
                animate={{
                    x: [0, -30, 0],
                    y: [0, -40, 0],
                }}
                transition={{
                    duration: 22,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="absolute -bottom-32 -right-32 w-[420px] h-[420px] rounded-full opacity-25 blur-3xl"
                style={{ background: "var(--accent)" }}
            />

            <motion.div
                animate={{
                    x: [0, 20, 0],
                    y: [0, -20, 0],
                }}
                transition={{
                    duration: 15,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="absolute top-1/3 right-1/4 w-[280px] h-[280px] rounded-full opacity-20 blur-3xl"
                style={{ background: "var(--success)" }}
            />

            {/* Glassmorphism card -- semi-transparent surface color +
                backdrop-blur, so the orbs behind it stay faintly
                visible through the card instead of being fully
                hidden. Pairs with the orbs rather than just sitting
                flatly on top of them. */}
            <motion.div
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, ease: "easeOut" }}
                className="
                    relative z-10
                    bg-[var(--surface)]/70
                    backdrop-blur-xl
                    border border-[var(--border)]
                    shadow-[var(--shadow)]
                    rounded-2xl
                    w-full max-w-md p-8
                "
            >

                <div className="text-center mb-8">

                    <div
                        className="
                            w-14 h-14 mx-auto mb-4
                            rounded-2xl
                            flex items-center justify-center
                            bg-[var(--primary)]
                        "
                    >
                        <Wallet
                            size={26}
                            className="text-white"
                        />
                    </div>

                    <h1 className="text-3xl font-bold text-blue-600">
                        SmartBudget AI
                    </h1>

                    <p className="text-[var(--text-light)] mt-2">
                        {title}
                    </p>

                </div>

                {children}

            </motion.div>

        </div>
    );
}