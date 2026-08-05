import { Search } from "lucide-react";

export default function TransactionFilters() {

    return (

        <div className="mt-8 flex gap-4">

            <div className="relative flex-1">

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
                    placeholder="Search transactions..."
                    className="
                        w-full
                        pl-11
                        pr-4
                        py-3
                        rounded-xl
                        border
                        outline-none
                    "
                />

            </div>

            <select
                className="px-4 rounded-xl border"
            >
                <option>All Categories</option>
            </select>

            <select
                className="px-4 rounded-xl border"
            >
                <option>All Types</option>
            </select>

        </div>

    );

}