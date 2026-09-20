import { Sun, Moon } from "lucide-react";
import { useTheme } from "../../context/ThemeContext";

export default function ThemeToggleButton() {

    const { theme, toggleTheme } = useTheme();

    return (

        <button
            type="button"
            onClick={toggleTheme}
            title={
                theme === "dark"
                    ? "Switch to light mode"
                    : "Switch to dark mode"
            }
            className="
                fixed
                top-6
                right-6
                z-50
                w-12
                h-12
                rounded-full
                flex
                items-center
                justify-center
                bg-[var(--surface)]
                border
                border-[var(--border)]
                text-[var(--text-light)]
                shadow-[var(--shadow)]
                hover:scale-105
                hover:text-[var(--text)]
                transition-all
                duration-300
            "
        >
            {theme === "dark" ? (
                <Sun size={20} />
            ) : (
                <Moon size={20} />
            )}
        </button>

    );

}