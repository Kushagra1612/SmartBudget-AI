import { Link } from "react-router-dom";
import { Wallet } from "lucide-react";

export default function LandingFooter() {

    return (

        <footer className="border-t border-[var(--border)] py-12 px-6">

            <div className="
                max-w-7xl mx-auto
                flex flex-col sm:flex-row
                items-center justify-between
                gap-6
            ">

                {/* Logo */}
                <div className="flex items-center gap-3">

                    <div className="
                        w-8 h-8 rounded-lg
                        bg-[var(--primary)]
                        flex items-center justify-center
                    ">
                        <Wallet size={16} className="text-white" />
                    </div>

                    <span className="text-sm font-semibold text-[var(--text)]">
                        SmartBudget AI
                    </span>

                </div>

                {/* Links */}
                <div className="
                    flex items-center gap-6
                    text-sm text-[var(--text-light)]
                ">

                    <a
                        href="#features"
                        className="hover:text-[var(--text)] transition-colors"
                    >
                        Features
                    </a>

                    <Link
                        to="/login"
                        className="hover:text-[var(--text)] transition-colors"
                    >
                        Log in
                    </Link>

                    <Link
                        to="/register"
                        className="hover:text-[var(--text)] transition-colors"
                    >
                        Sign up
                    </Link>

                </div>

            </div>

        </footer>

    );

}
