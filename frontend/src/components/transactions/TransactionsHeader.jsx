import { Plus } from "lucide-react";

export default function TransactionsHeader() {

    return (

        <div className="flex items-center justify-between">

            <div>

                <h1 className="text-4xl font-bold">
                    Transactions
                </h1>

                <p className="text-gray-500 mt-2">
                    Track every income and expense.
                </p>

            </div>

            <button
                className="
                    flex items-center gap-2
                    bg-[var(--primary)]
                    text-white
                    px-5 py-3
                    rounded-xl
                    font-semibold
                    hover:opacity-90
                    transition
                "
            >

                <Plus size={18}/>

                Add Transaction

            </button>

        </div>

    );

}