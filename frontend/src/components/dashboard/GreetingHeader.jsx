import { Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { Sparkles } from "lucide-react";
import { motion } from "framer-motion";

export default function GreetingHeader() {
    const { user } = useAuth();
    const hour = new Date().getHours();

    let greeting = "Good Evening";
    if (hour < 12) greeting = "Good Morning";
    else if (hour < 18) greeting = "Good Afternoon";

    const firstName = user?.full_name?.split(" ")[0];

    return (
        <div className="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
                <p className="text-xs font-semibold tracking-wider uppercase text-[var(--text-light)]">
                    {new Date().toLocaleDateString("en-IN", {
                        weekday: "long",
                        day: "numeric",
                        month: "long",
                    })}
                </p>

                <h1 className="mt-1 text-3xl sm:text-4xl font-extrabold tracking-tight text-[var(--text)]">
                    {greeting}{firstName ? `, ${firstName}` : ""} 👋
                </h1>

                <p className="mt-1 text-sm text-[var(--text-light)]">
                    Here's what's happening with your finances today.
                </p>
            </div>

            {/* Quick action shortcuts */}
            <div className="flex items-center gap-3 self-start sm:self-auto">
                <Link to="/ai">
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="
                            inline-flex items-center gap-2 px-4 py-2.5 rounded-xl
                            text-sm font-semibold
                            bg-[var(--primary)] text-white
                            shadow-md shadow-[var(--primary)]/20
                            hover:brightness-110
                            transition-all
                        "
                    >
                        <Sparkles size={16} />
                        <span>Ask AI</span>
                    </motion.button>
                </Link>
            </div>
        </div>
    );
}