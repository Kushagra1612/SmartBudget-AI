import { useState } from "react";
import { Upload, FileText } from "lucide-react";
import { useNavigate } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";
import { uploadStatement } from "../api/upload";

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

            alert("Please select a PDF statement.");

            return;

        }

        try {

            setLoading(true);

            const result = await uploadStatement(file);

            alert(
                `${result.transactions_found} transactions imported successfully.`
            );

            navigate("/transactions");

        } catch (err) {

            alert(
                err.response?.data?.detail ??
                "Upload failed."
            );

        } finally {

            setLoading(false);

        }

    }

    return (

        <MainLayout>

            <div className="max-w-2xl mx-auto">

                <h1 className="text-4xl font-bold mb-2">
                    Upload Bank Statement
                </h1>

                <p className="text-gray-500 mb-8">
                    Upload your PDF bank statement to automatically extract transactions using AI.
                </p>

                <div className="bg-white rounded-2xl shadow-lg p-10">

                    <div className="flex flex-col items-center">

                        <Upload
                            size={60}
                            className="text-blue-600 mb-6"
                        />

                        <label
                            className="
                                cursor-pointer
                                border-2
                                border-dashed
                                border-gray-300
                                rounded-xl
                                w-full
                                p-10
                                text-center
                                hover:border-blue-500
                                transition
                            "
                        >

                            <FileText
                                size={42}
                                className="mx-auto mb-4"
                            />

                            <p className="font-semibold">
                                Click to choose a PDF
                            </p>

                            <p className="text-sm text-gray-500 mt-2">
                                Maximum size: 10 MB
                            </p>

                            <input
                                type="file"
                                accept=".pdf"
                                className="hidden"
                                onChange={handleFileChange}
                            />

                        </label>

                        {file && (

                            <div className="mt-6 text-center">

                                <p className="font-semibold">
                                    {file.name}
                                </p>

                                <p className="text-sm text-gray-500">
                                    {(file.size / 1024 / 1024).toFixed(2)} MB
                                </p>

                            </div>

                        )}

                        <button
                            onClick={handleUpload}
                            disabled={loading}
                            className="
                                mt-8
                                bg-blue-600
                                hover:bg-blue-700
                                text-white
                                px-8
                                py-3
                                rounded-xl
                                transition
                            "
                        >

                            {loading
                                ? "Uploading..."
                                : "Upload Statement"}

                        </button>

                    </div>

                </div>

            </div>

        </MainLayout>

    );

}