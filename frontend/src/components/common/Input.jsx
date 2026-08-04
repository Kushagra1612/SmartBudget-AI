import { motion } from "framer-motion";

export default function Input({
    label,
    type = "text",
    placeholder,
    value,
    onChange,
    icon: Icon,
    error,
}) {
    return (
        <div className="w-full">

            {label && (
                <label className="block mb-2 text-sm font-semibold text-[var(--text)]">
                    {label}
                </label>
            )}

            <motion.div
                whileFocus={{ scale: 1.01 }}
                className={`
                    flex
                    items-center
                    gap-3
                    bg-white
                    border
                    rounded-2xl
                    px-4
                    py-3
                    shadow-sm
                    transition-all
                    ${error
                        ? "border-red-500"
                        : "border-gray-200 focus-within:border-[var(--primary)]"}
                `}
            >
                {Icon && (
                    <Icon
                        size={20}
                        className="text-gray-400"
                    />
                )}

                <input
                    className="
                        flex-1
                        outline-none
                        bg-transparent
                        text-[var(--text)]
                        placeholder:text-gray-400
                    "
                    type={type}
                    placeholder={placeholder}
                    value={value}
                    onChange={onChange}
                />
            </motion.div>

            {error && (
                <p className="mt-2 text-sm text-red-500">
                    {error}
                </p>
            )}

        </div>
    );
}