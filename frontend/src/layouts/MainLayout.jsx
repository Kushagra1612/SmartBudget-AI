import FloatingDock from "../components/common/FloatingDock";

export default function MainLayout({ children }) {

    return (

        <div className="min-h-screen bg-[var(--bg)]">

             <main className="w-full min-h-screen px-10 py-8 pb-32">
                {children}
             </main>

            <FloatingDock />

        </div>

    );

}