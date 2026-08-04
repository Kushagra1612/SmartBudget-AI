import { motion } from "framer-motion";

export default function Card({
    children,
    className = "",
    hover = true,
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
            className={`
                bg-white
                rounded-[28px]
                p-6
                shadow-[0_12px_40px_rgba(15,23,42,0.08)]
                border
                border-gray-100
                overflow-hidden
                ${className}
            `}
        >
            {children}
        </motion.div>
    );
}