import Card from "../common/Card";
import useAIPulse from "../../hooks/useAIPulse";

export default function AIPulseCard() {

    const {
        pulse,
        loading,
    } = useAIPulse();

    if (loading) {
        return (
            <Card>
                Loading AI insights...
            </Card>
        );
    }

    if (!pulse) {
        return (
            <Card>
                <h2 className="text-2xl font-bold">
                    AI Daily Pulse
                </h2>

                <p className="mt-6 text-gray-500">
                    Unable to load AI insights.
                </p>
            </Card>
        );
    }

    return (

    <Card>

        <h2 className="text-2xl font-bold">
            AI Daily Pulse
        </h2>

        <div className="mt-6">

            <p className="text-lg">
                {pulse.message}
            </p>

            <div className="mt-4">

                <span
                    className={`
                        inline-block
                        px-3
                        py-1
                        rounded-full
                        text-sm
                        font-semibold
                        ${
                            pulse.status === "Excellent"
                                ? "bg-green-100 text-green-700"
                                : pulse.status === "Very Good"
                                ? "bg-emerald-100 text-emerald-700"
                                : pulse.status === "Good"
                                ? "bg-blue-100 text-blue-700"
                                : pulse.status === "Average"
                                ? "bg-yellow-100 text-yellow-700"
                                : "bg-red-100 text-red-700"
                        }
                    `}
                >
                    {pulse.status}
                </span>

            </div>

        </div>

    </Card>

);

}