import { motion } from "framer-motion";

export default function Button({
    children,
    onClick,
    type = "button",
    variant = "primary",
    disabled = false,
    className = "",
}) {
    const variants = {
        primary:
            "bg-[var(--primary)] text-white hover:brightness-110",

        secondary:
            "bg-white text-[var(--text)] border border-gray-200 hover:bg-gray-50",

        danger:
            "bg-[var(--danger)] text-white hover:brightness-110",
    };

    return (
        <motion.button
            whileHover={{
                scale: 1.02,
            }}
            whileTap={{
                scale: 0.97,
            }}
            type={type}
            disabled={disabled}
            onClick={onClick}
            className={`
                px-6
                py-3
                rounded-2xl
                font-semibold
                transition-all
                duration-300
                shadow-sm
                disabled:opacity-50
                disabled:cursor-not-allowed
                ${variants[variant]}
                ${className}
            `}
        >
            {children}
        </motion.button>
    );
}