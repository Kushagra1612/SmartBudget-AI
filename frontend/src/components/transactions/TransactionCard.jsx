import { useState } from "react";
import { Pencil } from "lucide-react";
import toast from "react-hot-toast";

import { updateTransaction } from "../../api/transaction";
import { TRANSACTION_CATEGORIES } from "../../constants/categories";
import { formatRupees } from "../../utils/currency";

export default function TransactionCard({
    transaction,
    onUpdated,
}) {

    const isIncome =
        transaction.transaction_type === "Income";

    const [editing, setEditing] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [category, setCategory] = useState(transaction.category);
    const [merchant, setMerchant] = useState(transaction.merchant);

    function startEditing() {

        setCategory(transaction.category);
        setMerchant(transaction.merchant);
        setEditing(true);

    }

    async function handleSave(e) {

        e.preventDefault();

        try {

            setSubmitting(true);

            await updateTransaction(transaction.id, {
                category,
                merchant: merchant.trim() || "UNKNOWN",
            });

            toast.success("Transaction updated.");

            setEditing(false);

            onUpdated();

        } catch {

            toast.error("Failed to update transaction.");

        } finally {

            setSubmitting(false);

        }

    }

    return (

        <div
            className="
                bg-[var(--surface)]
                text-[var(--text)]
                border
                border-[var(--border)]
                rounded-2xl
                shadow-[var(--shadow)]
                p-5
                transition
            "
        >

            <div className="flex justify-between items-start">

                <div className="flex-1">

                    {editing ? (

                        <input
                            value={merchant}
                            onChange={(e) => setMerchant(e.target.value)}
                            placeholder="Merchant name"
                            className="
                                text-lg
                                font-semibold
                                bg-[var(--surface)]
                                text-[var(--text)]
                                border
                                border-[var(--border)]
                                rounded-lg
                                px-2
                                py-1
                                w-full
                            "
                        />

                    ) : (

                        <h3 className="text-lg font-semibold">
                            {transaction.merchant}
                        </h3>

                    )}

                    <p className="text-sm text-[var(--text-light)] mt-1">
                        {transaction.description || "No description"}
                    </p>

                </div>

                <div className="flex items-center gap-2 ml-3">

                    <span
                        className={`
                            px-3
                            py-1
                            rounded-full
                            text-sm
                            font-medium
                            whitespace-nowrap
                            ${
                                isIncome
                                    ? "bg-green-100 text-green-700"
                                    : "bg-red-100 text-red-700"
                            }
                        `}
                    >
                        {transaction.transaction_type}
                    </span>

                    {!editing && (

                        <button
                            onClick={startEditing}
                            title="Edit category / merchant"
                            className="
                                text-[var(--text-light)]
                                hover:text-[var(--text)]
                                transition
                            "
                        >
                            <Pencil size={16} />
                        </button>

                    )}

                </div>

            </div>

            <div className="mt-5 flex justify-between items-end">

                <div>

                    <p className="text-sm text-[var(--text-light)]">
                        Category
                    </p>

                    {editing ? (

                        <select
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            className="
                                font-medium
                                bg-[var(--surface)]
                                text-[var(--text)]
                                border
                                border-[var(--border)]
                                rounded-lg
                                px-2
                                py-1
                                mt-1
                            "
                        >

                            {TRANSACTION_CATEGORIES.map((option) => (

                                <option
                                    key={option}
                                    value={option}
                                >
                                    {option}
                                </option>

                            ))}

                        </select>

                    ) : (

                        <p className="font-medium">
                            {transaction.category}
                        </p>

                    )}

                </div>

                <div>

                    <p className="text-sm text-[var(--text-light)]">
                        Payment
                    </p>

                    <p className="font-medium">
                        {transaction.payment_mode || "-"}
                    </p>

                </div>

            </div>

            <div className="mt-5 flex justify-between items-end">

                <div>

                    <p className="text-sm text-[var(--text-light)]">
                        Date
                    </p>

                    <p className="font-medium">
                        {transaction.transaction_date}
                    </p>

                </div>

                <p
                    className={`text-xl font-bold ${
                        isIncome
                            ? "text-green-600"
                            : "text-red-600"
                    }`}
                >
                    {formatRupees(transaction.amount)}
                </p>

            </div>

            {editing && (

                <div className="flex gap-3 mt-5">

                    <button
                        onClick={handleSave}
                        disabled={submitting}
                        className="
                            flex-1
                            bg-blue-600
                            hover:bg-blue-700
                            text-white
                            py-2
                            rounded-lg
                        "
                    >
                        {submitting ? "Saving..." : "Save"}
                    </button>

                    <button
                        onClick={() => setEditing(false)}
                        disabled={submitting}
                        className="
                            flex-1
                            bg-[var(--bg)]
                            hover:opacity-80
                            text-[var(--text)]
                            border
                            border-[var(--border)]
                            py-2
                            rounded-lg
                        "
                    >
                        Cancel
                    </button>

                </div>

            )}

        </div>

    );

}