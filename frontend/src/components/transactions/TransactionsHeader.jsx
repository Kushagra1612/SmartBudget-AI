import { Upload } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function TransactionsHeader() {

    const navigate = useNavigate();

    return (

        <div className="flex items-center justify-between mb-8">

            <div>

                <h1 className="text-4xl font-bold">
                    Transactions
                </h1>

                <p className="text-gray-500 mt-2">
                    View and analyze all transactions imported from your bank statements.
                </p>

            </div>

            <button
                onClick={() => navigate("/upload")}
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

                <Upload size={18} />

                Upload Statement

            </button>

        </div>

    );

}