export default function AuthLayout({ title, children }) {
    return (
        <div className="min-h-screen bg-slate-100 flex items-center justify-center">

            <div className="bg-white shadow-xl rounded-2xl w-full max-w-md p-8">

                <div className="text-center mb-8">

                    <h1 className="text-3xl font-bold text-blue-600">
                        SmartBudget AI
                    </h1>

                    <p className="text-gray-500 mt-2">
                        {title}
                    </p>

                </div>

                {children}

            </div>

        </div>
    );
}