import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import toast from "react-hot-toast";
import { Trash2, FileText, Upload, Plus } from "lucide-react";

import MainLayout from "../layouts/MainLayout";
import Card from "../components/common/Card";
import useStatements from "../hooks/useStatements";
import { deleteStatement } from "../api/statements";

function formatUploadedAt(value) {

    return new Date(value).toLocaleDateString("en-IN", {
        day: "numeric",
        month: "short",
        year: "numeric",
    });

}

export default function Statements() {

    const {
        statements,
        loading,
        error,
        refetch,
    } = useStatements();

    const [deletingId, setDeletingId] = useState(null);

    async function handleDelete(statement) {

        if (
            !confirm(
                `Delete "${statement.original_filename}"? This will ` +
                `also delete all ${statement.transaction_count} ` +
                `transactions from this statement.`
            )
        ) {
            return;
        }

        try {

            setDeletingId(statement.id);

            await deleteStatement(statement.id);

            toast.success("Statement deleted.");

            refetch();

        } catch {

            toast.error("Failed to delete statement.");

        } finally {

            setDeletingId(null);

        }

    }

    if (loading) {
        return (
            <MainLayout>
                <p className="mt-10 text-center text-gray-500">
                    Loading statements...
                </p>
            </MainLayout>
        );
    }

    if (error) {
        return (
            <MainLayout>
                <p className="mt-10 text-center text-red-500">
                    Failed to load statements.
                </p>
            </MainLayout>
        );
    }

    return (

        <MainLayout>
            <div className="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-extrabold tracking-tight text-[var(--text)]">
                        Uploaded Statements
                    </h1>
                    <p className="mt-1 text-sm text-[var(--text-light)]">
                        Manage your bank statements and extracted transaction history.
                    </p>
                </div>

                <Link to="/upload">
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="
                            inline-flex items-center gap-2 px-5 py-2.5 rounded-xl
                            text-sm font-semibold
                            bg-[var(--primary)] text-white
                            shadow-md shadow-[var(--primary)]/20
                            hover:brightness-110
                            transition-all
                        "
                    >
                        <Plus size={16} />
                        <span>Upload Statement</span>
                    </motion.button>
                </Link>
            </div>

            {statements.length === 0 ? (
                <div className="text-center py-20 bg-[var(--surface)] border border-dashed border-[var(--border)] rounded-2xl p-10">
                    <div className="w-14 h-14 mx-auto rounded-2xl bg-[var(--primary)]/10 text-[var(--primary)] flex items-center justify-center mb-4">
                        <Upload size={24} />
                    </div>
                    <p className="text-lg font-bold text-[var(--text)]">
                        No statements uploaded yet
                    </p>
                    <p className="mt-1 text-sm text-[var(--text-light)] max-w-sm mx-auto">
                        Upload your bank statement PDF to extract and categorize your transactions with AI.
                    </p>
                    <Link to="/upload" className="inline-block mt-6">
                        <button
                            type="button"
                            className="px-6 py-2.5 rounded-xl text-sm font-semibold bg-[var(--primary)] text-white hover:brightness-110 shadow-sm"
                        >
                            Upload Your First Statement
                        </button>
                    </Link>
                </div>

            ) : (

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                    {statements.map((statement) => (

                        <Card key={statement.id}>

                            <div className="flex items-start justify-between">

                                <div className="flex items-start gap-3">

                                    <FileText
                                        size={28}
                                        className="text-[var(--primary)] mt-1"
                                    />

                                    <div>

                                        <h3 className="font-semibold break-all">
                                            {statement.original_filename}
                                        </h3>

                                        <p className="text-sm text-gray-500 mt-1">
                                            {statement.bank || "Unknown bank"}
                                        </p>

                                    </div>

                                </div>

                                <button
                                    onClick={() => handleDelete(statement)}
                                    disabled={deletingId === statement.id}
                                    title="Delete statement"
                                    className="
                                        text-gray-400
                                        hover:text-red-500
                                        transition
                                        shrink-0
                                    "
                                >
                                    <Trash2 size={18} />
                                </button>

                            </div>

                            <div className="mt-5 grid grid-cols-2 gap-3 text-sm">

                                <div>
                                    <p className="text-gray-500">Period</p>
                                    <p className="font-medium">
                                        {statement.month && statement.year
                                            ? `${statement.month}/${statement.year}`
                                            : "-"}
                                    </p>
                                </div>

                                <div>
                                    <p className="text-gray-500">Transactions</p>
                                    <p className="font-medium">
                                        {statement.transaction_count}
                                    </p>
                                </div>

                                <div>
                                    <p className="text-gray-500">Pages</p>
                                    <p className="font-medium">
                                        {statement.pages ?? "-"}
                                    </p>
                                </div>

                                <div>
                                    <p className="text-gray-500">Uploaded</p>
                                    <p className="font-medium">
                                        {formatUploadedAt(statement.uploaded_at)}
                                    </p>
                                </div>

                            </div>

                        </Card>

                    ))}

                </div>

            )}

        </MainLayout>

    );

}