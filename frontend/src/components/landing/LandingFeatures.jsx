import { motion } from "framer-motion";
import { Upload, Bot, Target, AlertTriangle } from "lucide-react";
import Card from "../common/Card";

const features = [
    {
        icon: Upload,
        title: "Upload & Parse Statements",
        description:
            "Upload any bank statement PDF and watch as AI extracts and categorizes every transaction automatically.",
        color: "bg-indigo-100 text-indigo-600 dark:bg-indigo-500/20 dark:text-indigo-400",
    },
    {
        icon: Bot,
        title: "AI-Powered Insights",
        description:
            "Get personalized financial advice from a multi-agent AI system powered by Google Gemini.",
        color: "bg-teal-100 text-teal-600 dark:bg-teal-500/20 dark:text-teal-400",
    },
    {
        icon: Target,
        title: "Budgets & Goals",
        description:
            "Set monthly budgets by category and track savings goals — the AI adapts recommendations as you progress.",
        color: "bg-green-100 text-green-600 dark:bg-green-500/20 dark:text-green-400",
    },
    {
        icon: AlertTriangle,
        title: "Anomaly Detection",
        description:
            "Machine learning spots unusual spending patterns and alerts you before small leaks become big problems.",
        color: "bg-amber-100 text-amber-600 dark:bg-amber-500/20 dark:text-amber-400",
    },
];

const container = {
    hidden: {},
    show: {
        transition: {
            staggerChildren: 0.15,
        },
    },
};

const item = {
    hidden: { opacity: 0, y: 24 },
    show: {
        opacity: 1,
        y: 0,
        transition: { duration: 0.5 },
    },
};

export default function LandingFeatures() {

    return (

        <section id="features" className="relative py-24 px-6">

            <div className="max-w-7xl mx-auto">

                {/* Section header */}
                <div className="text-center mb-16">

                    <h2 className="
                        text-3xl sm:text-4xl
                        font-bold text-[var(--text)]
                    ">
                        Everything you need to manage your finances
                    </h2>

                    <p className="
                        mt-4 text-lg
                        text-[var(--text-light)]
                        max-w-2xl mx-auto
                    ">
                        Built with real AI, real ML, and real data —
                        not just pretty charts.
                    </p>

                </div>

                {/* Feature cards grid */}
                <motion.div
                    variants={container}
                    initial="hidden"
                    whileInView="show"
                    viewport={{ once: true, amount: 0.2 }}
                    className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
                >
                    {features.map((feature) => {

                        const Icon = feature.icon;

                        return (
                            <motion.div
                                key={feature.title}
                                variants={item}
                            >
                                <Card className="h-full text-center p-8">

                                    <div className={`
                                        w-14 h-14 mx-auto rounded-2xl
                                        flex items-center justify-center
                                        ${feature.color}
                                    `}>
                                        <Icon size={24} />
                                    </div>

                                    <h3 className="
                                        mt-5 text-lg font-bold
                                        text-[var(--text)]
                                    ">
                                        {feature.title}
                                    </h3>

                                    <p className="
                                        mt-3 text-sm
                                        text-[var(--text-light)]
                                        leading-relaxed
                                    ">
                                        {feature.description}
                                    </p>

                                </Card>
                            </motion.div>
                        );

                    })}
                </motion.div>

            </div>

        </section>

    );

}
