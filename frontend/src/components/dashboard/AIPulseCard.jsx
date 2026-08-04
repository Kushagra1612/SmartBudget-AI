import { Bot } from "lucide-react";
import Card from "../common/Card";

export default function AIPulseCard() {
    return (
        <Card className="h-full">

            <div className="flex items-center gap-3">

                <div className="w-12 h-12 rounded-full bg-[var(--primary)] flex items-center justify-center">

                    <Bot className="text-white" size={22} />

                </div>

                <div>

                    <h2 className="text-xl font-bold">
                        AI Daily Pulse
                    </h2>

                    <p className="text-sm text-gray-500">
                        Personalized financial insight
                    </p>

                </div>

            </div>

            <div className="mt-8">

                <p className="text-lg leading-8 text-gray-700">

                    🎯 You spent
                    <span className="font-bold">
                        {" "}₹1,850 less{" "}
                    </span>
                    on dining this month.

                    <br /><br />

                    At your current pace,
                    you'll reach your Laptop Goal
                    <span className="font-bold">
                        {" "}18 days earlier.
                    </span>

                </p>

            </div>

        </Card>
    );
}