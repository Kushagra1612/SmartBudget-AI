import Sidebar from "../components/common/Sidebar";

export default function MainLayout({ children }) {
    return (
        <div className="relative min-h-screen bg-[var(--bg)]">
            {/* Subtle background ambient glow orbs */}
            <div
                className="fixed -top-32 -left-32 w-[420px] h-[420px] rounded-full opacity-10 blur-3xl pointer-events-none"
                style={{ background: "var(--primary)" }}
            />
            <div
                className="fixed -bottom-32 -right-32 w-[420px] h-[420px] rounded-full opacity-10 blur-3xl pointer-events-none"
                style={{ background: "var(--accent)" }}
            />

            {/* Left Sidebar (fixed on desktop, drawer on mobile) */}
            <Sidebar />

            {/* Main scrollable content zone */}
            <div className="lg:pl-64 flex flex-col min-h-screen">
                <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-8 py-8 pt-20 lg:pt-10 pb-16">
                    {children}
                </main>
            </div>
        </div>
    );
}