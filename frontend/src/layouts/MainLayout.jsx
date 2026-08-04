import FloatingDock from "../components/common/FloatingDock";

export default function MainLayout({ children }) {

    return (

        <div className="min-h-screen bg-[var(--bg)]">

            <main className="max-w-7xl mx-auto px-8 py-10 pb-32">

                {children}

            </main>

            <FloatingDock />

        </div>

    );

}