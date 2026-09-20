import { motion } from "framer-motion";

export default function Card({
    children,
    className = "",
    hover = true,
    style,
}) {
    return (
        <motion.div
            whileHover={
                hover
                    ? {
                          y: -6,
                          scale: 1.015,
                      }
                    : {}
            }
            transition={{
                duration: 0.25,
            }}
            style={style}
            className={`
                bg-[var(--surface)]
                rounded-[28px]
                p-6
                shadow-[var(--shadow)]
                border
                border-[var(--border)]
                overflow-hidden
                ${className}
            `}
        >
            {children}
        </motion.div>
    );
}