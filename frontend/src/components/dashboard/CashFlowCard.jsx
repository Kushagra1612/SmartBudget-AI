import Card from "../common/Card";
import { formatRupees } from "../../utils/currency";
import { TrendingUp, TrendingDown, PiggyBank } from "lucide-react";

export default function CashFlowCard({
    title,
    amount,
    change,
    positive = true,
}) {
    const isNegative = Number(amount) < 0;

    const iconMap = {
        Income: {
            icon: TrendingUp,
            bg: "bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400",
            border: "hover:border-emerald-500/30",
        },
        Expenses: {
            icon: TrendingDown,
            bg: "bg-rose-100 dark:bg-rose-500/20 text-rose-600 dark:text-rose-400",
            border: "hover:border-rose-500/30",
        },
        Savings: {
            icon: PiggyBank,
            bg: "bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400",
            border: "hover:border-indigo-500/30",
        },
    };

    const style = iconMap[title] || {
        icon: TrendingUp,
        bg: "bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400",
        border: "hover:border-blue-500/30",
    };

    const Icon = style.icon;

    return (
        <Card className={`relative overflow-hidden transition-all duration-300 ${style.border}`}>
            <div className="flex items-center justify-between">
                <p className="text-sm font-semibold text-[var(--text-light)] tracking-wide">
                    {title}
                </p>
                <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${style.bg}`}>
                    <Icon size={18} />
                </div>
            </div>

            <h2
                className={`text-3xl font-extrabold tracking-tight mt-4 text-[var(--text)] ${
                    isNegative ? "text-rose-600 dark:text-rose-400" : ""
                }`}
            >
                {formatRupees(amount)}
            </h2>

            {change && (
                <div className="mt-3">
                    <span
                        className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                            positive
                                ? "bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-300"
                                : "bg-rose-100 dark:bg-rose-500/20 text-rose-700 dark:text-rose-300"
                        }`}
                    >
                        {change}
                    </span>
                </div>
            )}
        </Card>
    );
}