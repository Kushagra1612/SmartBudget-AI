import { motion } from "framer-motion";
import { Bot, Sparkles, Cpu, Network, ShieldAlert, LineChart } from "lucide-react";
import Card from "../common/Card";

export default function LandingAITeaser() {
    return (
        <section className="relative py-16 px-6 max-w-7xl mx-auto">
            {/* Tech strip */}
            <div className="mb-20 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="flex items-center gap-3 p-4 rounded-2xl bg-[var(--surface)] border border-[var(--border)]">
                    <div className="w-10 h-10 rounded-xl bg-purple-100 dark:bg-purple-500/20 text-purple-600 flex items-center justify-center shrink-0">
                        <Network size={20} />
                    </div>
                    <div>
                        <p className="text-xs text-[var(--text-light)]">Architecture</p>
                        <p className="text-sm font-bold text-[var(--text)]">LangGraph 4-Agent</p>
                    </div>
                </div>

                <div className="flex items-center gap-3 p-4 rounded-2xl bg-[var(--surface)] border border-[var(--border)]">
                    <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-500/20 text-blue-600 flex items-center justify-center shrink-0">
                        <Cpu size={20} />
                    </div>
                    <div>
                        <p className="text-xs text-[var(--text-light)]">Intelligence</p>
                        <p className="text-sm font-bold text-[var(--text)]">Google Gemini API</p>
                    </div>
                </div>

                <div className="flex items-center gap-3 p-4 rounded-2xl bg-[var(--surface)] border border-[var(--border)]">
                    <div className="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-500/20 text-amber-600 flex items-center justify-center shrink-0">
                        <ShieldAlert size={20} />
                    </div>
                    <div>
                        <p className="text-xs text-[var(--text-light)]">ML Model</p>
                        <p className="text-sm font-bold text-[var(--text)]">Isolation Forest</p>
                    </div>
                </div>

                <div className="flex items-center gap-3 p-4 rounded-2xl bg-[var(--surface)] border border-[var(--border)]">
                    <div className="w-10 h-10 rounded-xl bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 flex items-center justify-center shrink-0">
                        <LineChart size={20} />
                    </div>
                    <div>
                        <p className="text-xs text-[var(--text-light)]">Parsing</p>
                        <p className="text-sm font-bold text-[var(--text)]">Automated PDF Tables</p>
                    </div>
                </div>
            </div>

            {/* Showcase header */}
            <div className="text-center mb-12">
                <span className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full text-xs font-semibold bg-purple-100 text-purple-700 dark:bg-purple-500/20 dark:text-purple-300">
                    <Sparkles size={14} />
                    Multi-Agent Pipeline
                </span>
                <h2 className="mt-4 text-3xl sm:text-4xl font-bold text-[var(--text)]">
                    Ask anything. Specialist agents handle the rest.
                </h2>
                <p className="mt-3 text-[var(--text-light)] max-w-xl mx-auto">
                    Instead of generic chat, a coordinator agent routes your question to dedicated specialist agents running in parallel.
                </p>
            </div>

            {/* Interactive / visual agent simulation card */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className="max-w-3xl mx-auto"
            >
                <Card hover={false} className="p-6 sm:p-8 relative overflow-hidden">
                    {/* Simulated user prompt */}
                    <div className="flex items-start gap-4 mb-6">
                        <div className="w-9 h-9 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-sm shrink-0">
                            You
                        </div>
                        <div className="bg-[var(--bg)] border border-[var(--border)] rounded-2xl rounded-tl-none px-4 py-3 text-sm text-[var(--text)] max-w-md">
                            "Where am I overspending this month, and how can I save ₹3,000 more for my laptop goal?"
                        </div>
                    </div>

                    {/* Agent coordinator routing badge */}
                    <div className="ml-13 mb-6 flex flex-wrap items-center gap-2 text-xs">
                        <span className="px-2.5 py-1 rounded-lg bg-[var(--primary)]/10 text-[var(--primary)] font-semibold flex items-center gap-1.5">
                            <Network size={13} />
                            Coordinator Agent
                        </span>
                        <span className="text-[var(--text-light)]">routed in parallel to:</span>
                        <span className="px-2.5 py-1 rounded-lg bg-teal-100 dark:bg-teal-500/20 text-teal-700 dark:text-teal-300 font-medium">
                            Spending Agent
                        </span>
                        <span className="px-2.5 py-1 rounded-lg bg-emerald-100 dark:bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 font-medium">
                            Goal Agent
                        </span>
                    </div>

                    {/* Multi-agent combined answer */}
                    <div className="flex items-start gap-4">
                        <div className="w-9 h-9 rounded-full bg-[var(--primary)] text-white flex items-center justify-center shrink-0">
                            <Bot size={18} />
                        </div>
                        <div className="space-y-3 bg-[var(--bg)] border border-[var(--border)] rounded-2xl rounded-tl-none p-5 text-sm text-[var(--text)] flex-1">
                            <p className="font-semibold text-base flex items-center gap-2">
                                <Sparkles size={16} className="text-amber-500" />
                                Smart Financial Synthesis:
                            </p>
                            <div className="space-y-2 text-[var(--text-light)] leading-relaxed">
                                <p>
                                    1. <strong className="text-[var(--text)]">Outlier Detected:</strong> Your spend in <code className="px-1.5 py-0.5 rounded bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300 text-xs font-mono">Other</code> hit ₹23,183 (23.4x your standard baseline).
                                </p>
                                <p>
                                    2. <strong className="text-[var(--text)]">Savings Opportunity:</strong> Trimming recurring utility extras by 12% recovers <strong className="text-[var(--success)]">₹3,200</strong> immediately.
                                </p>
                                <p>
                                    3. <strong className="text-[var(--text)]">Goal Impact:</strong> Allocating this to your <strong className="text-[var(--primary)]">Laptop Goal</strong> increases completion progress from 0% to 64% ahead of schedule!
                                </p>
                            </div>
                        </div>
                    </div>
                </Card>
            </motion.div>
        </section>
    );
}
