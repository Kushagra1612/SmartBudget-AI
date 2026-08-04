import { Target, CalendarDays } from "lucide-react";
import Card from "../common/Card";
import Button from "../common/Button";

export default function GoalsPreview({
    title = "Gaming Laptop",
    progress = 68,
    current = "68,000",
    target = "100,000",
    remaining = "32,000",
    recommendation = "Save ₹8,000/month to stay on track.",
}) {
    return (
        <Card>

            <div className="flex items-center justify-between">

                <div className="flex items-center gap-3">

                    <div className="w-12 h-12 rounded-xl bg-[var(--accent)] flex items-center justify-center">

                        <Target className="text-white" />

                    </div>

                    <div>

                        <h2 className="text-xl font-bold">
                            {title}
                        </h2>

                        <p className="text-gray-500">
                            Financial Goal
                        </p>

                    </div>

                </div>

                <span className="font-bold text-[var(--primary)]">
                    {progress}%
                </span>

            </div>

            <div className="mt-8">

                <div className="h-3 rounded-full bg-gray-200">

                    <div
                        className="h-full rounded-full bg-[var(--primary)]"
                        style={{
                            width: `${progress}%`,
                        }}
                    />

                </div>

            </div>

            <div className="grid grid-cols-2 gap-6 mt-8">

                <div>

                    <p className="text-gray-500">
                        Saved
                    </p>

                    <h3 className="text-2xl font-bold">
                        ₹{current}
                    </h3>

                </div>

                <div>

                    <p className="text-gray-500">
                        Target
                    </p>

                    <h3 className="text-2xl font-bold">
                        ₹{target}
                    </h3>

                </div>

            </div>

            <div className="mt-8 flex items-center gap-3">

                <CalendarDays
                    size={20}
                    className="text-gray-400"
                />

                <span>

                    Remaining:
                    <strong>
                        {" "}₹{remaining}
                    </strong>

                </span>

            </div>

            <div className="mt-8 rounded-2xl bg-indigo-50 p-5">

                <p className="font-semibold text-[var(--primary)]">

                    🤖 AI Recommendation

                </p>

                <p className="mt-2 text-gray-600">

                    {recommendation}

                </p>

            </div>

            <div className="mt-8">

                <Button className="w-full">

                    View Goal

                </Button>

            </div>

        </Card>
    );
}