import { Search } from "lucide-react";
import { TRANSACTION_CATEGORIES } from "../../constants/categories";

export default function TransactionFilters({
    search,
    setSearch,
    category,
    setCategory,
    type,
    setType,
    dateFrom,
    setDateFrom,
    dateTo,
    setDateTo,
}) {

    return (

        <div className="mt-8 flex flex-wrap gap-4">

            <div className="relative flex-1 min-w-[200px]">

                <Search
                    className="
                        absolute
                        left-4
                        top-1/2
                        -translate-y-1/2
                        text-gray-400
                    "
                    size={18}
                />

                <input
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    placeholder="Search transactions..."
                    className="
                        w-full
                        pl-11
                        pr-4
                        py-3
                        rounded-xl
                        border
                        border-[var(--border)]
                        bg-[var(--surface)]
                        text-[var(--text)]
                        outline-none
                    "
                />

            </div>

            <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="px-4 rounded-xl border border-[var(--border)] bg-[var(--surface)] text-[var(--text)]"
            >

                <option value="">
                    All Categories
                </option>

                {TRANSACTION_CATEGORIES.map((category) => (

                    <option
                        key={category}
                        value={category}
                    >
                        {category}
                    </option>

                ))}

            </select>

            <select
                value={type}
                onChange={(e) => setType(e.target.value)}
                className="px-4 rounded-xl border border-[var(--border)] bg-[var(--surface)] text-[var(--text)]"
            >

                <option value="">
                    All Types
                </option>

                <option value="Income">
                    Income
                </option>

                <option value="Expense">
                    Expense
                </option>

                <option value="Transfer">
                    Transfer
                </option>

            </select>

            <input
                type="date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                title="From date"
                className="px-4 py-3 rounded-xl border border-[var(--border)] bg-[var(--surface)] text-[var(--text)]"
            />

            <input
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                title="To date"
                className="px-4 py-3 rounded-xl border border-[var(--border)] bg-[var(--surface)] text-[var(--text)]"
            />

            {(dateFrom || dateTo) && (

                <button
                    onClick={() => {
                        setDateFrom("");
                        setDateTo("");
                    }}
                    className="px-4 rounded-xl border border-[var(--border)] text-[var(--text-light)] hover:text-[var(--text)]"
                >
                    Clear dates
                </button>

            )}

        </div>

    );

}