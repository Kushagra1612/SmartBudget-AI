import LandingNavbar from "../components/landing/LandingNavbar";
import LandingHero from "../components/landing/LandingHero";
import LandingAITeaser from "../components/landing/LandingAITeaser";
import LandingFeatures from "../components/landing/LandingFeatures";
import LandingFooter from "../components/landing/LandingFooter";

export default function LandingPage() {
    return (
        <div className="min-h-screen bg-[var(--bg)] text-[var(--text)] selection:bg-[var(--primary)] selection:text-white">
            <LandingNavbar />
            <main>
                <LandingHero />
                <LandingAITeaser />
                <LandingFeatures />
            </main>
            <LandingFooter />
        </div>
    );
}
