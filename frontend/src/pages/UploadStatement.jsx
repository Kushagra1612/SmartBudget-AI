import { useState } from "react";
import { Upload, FileText, CheckCircle2, ShieldCheck, Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import toast from "react-hot-toast";

import MainLayout from "../layouts/MainLayout";
import { uploadStatement } from "../api/upload";
import Card from "../components/common/Card";

export default function UploadStatement() {

    const navigate = useNavigate();

    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    function handleFileChange(e) {
        if (e.target.files.length > 0) {
            setFile(e.target.files[0]);
        }
    }

    async function handleUpload() {
        if (!file) {
            toast.error("Please select a PDF statement.");
            return;
        }

        try {
            setLoading(true);
            const result = await uploadStatement(file);
            toast.success(
                `${result.transactions_found ?? 0} transactions imported and categorized successfully.`
            );
            navigate("/transactions");
        } catch (err) {
            toast.error(
                err.response?.data?.detail ??
                "Upload failed. Please ensure the PDF is a valid bank statement."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <MainLayout>
            <div className="max-w-2xl mx-auto py-4">

                <div className="mb-8">
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-700 dark:bg-indigo-500/20 dark:text-indigo-300 mb-3">
                        <Sparkles size={13} />
                        Automated Transaction Extraction
                    </span>
                    <h1 className="text-3xl sm:text-4xl font-bold text-[var(--text)]">
                        Upload Bank Statement
                    </h1>
                    <p className="text-[var(--text-light)] mt-2">
                        Upload your PDF bank statement to extract, parse, and categorize your transactions automatically using AI.
                    </p>
                </div>

                <Card hover={false} className="p-8 sm:p-10">
                    <div className="flex flex-col items-center">

                        <div className="w-16 h-16 rounded-2xl bg-[var(--primary)]/10 text-[var(--primary)] flex items-center justify-center mb-6">
                            <Upload size={32} />
                        </div>

                        <label
                            className="
                                cursor-pointer
                                border-2
                                border-dashed
                                border-[var(--border)]
                                hover:border-[var(--primary)]
                                rounded-2xl
                                w-full
                                p-8 sm:p-12
                                text-center
                                bg-[var(--bg)]/50
                                hover:bg-[var(--bg)]
                                transition-all
                                duration-300
                            "
                        >
                            <FileText
                                size={40}
                                className="mx-auto mb-4 text-[var(--text-light)]"
                            />

                            <p className="font-semibold text-[var(--text)] text-base">
                                {file ? file.name : "Click to select or drop a PDF statement"}
                            </p>

                            <p className="text-xs text-[var(--text-light)] mt-2">
                                Supported formats: Standard PDF bank statements (Max: 10 MB)
                            </p>

                            <input
                                type="file"
                                accept=".pdf"
                                className="hidden"
                                onChange={handleFileChange}
                            />
                        </label>

                        {file && (
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="mt-6 flex items-center gap-3 px-4 py-2.5 rounded-xl bg-emerald-100/50 dark:bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 text-sm font-medium border border-emerald-300/40 dark:border-emerald-500/20"
                            >
                                <CheckCircle2 size={18} />
                                <span>{file.name}</span>
                                <span className="text-xs opacity-70">
                                    ({(file.size / 1024 / 1024).toFixed(2)} MB)
                                </span>
                            </motion.div>
                        )}

                        <motion.button
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={handleUpload}
                            disabled={loading || !file}
                            className="
                                mt-8
                                bg-[var(--primary)]
                                text-white
                                px-8
                                py-3.5
                                rounded-2xl
                                font-semibold
                                hover:brightness-110
                                disabled:opacity-50
                                disabled:cursor-not-allowed
                                transition-all
                                shadow-lg shadow-[var(--primary)]/20
                            "
                        >
                            {loading ? "Processing Statement..." : "Upload & Extract Transactions"}
                        </motion.button>

                    </div>

                    {/* Privacy notice */}
                    <div className="mt-8 pt-6 border-t border-[var(--border)] flex items-center justify-center gap-2 text-xs text-[var(--text-light)]">
                        <ShieldCheck size={16} className="text-green-500" />
                        <span>Encrypted parsing — statements are processed securely and never shared.</span>
                    </div>
                </Card>

            </div>
        </MainLayout>
    );
}