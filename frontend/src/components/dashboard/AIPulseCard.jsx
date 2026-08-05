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

            <p className="mt-6">
                {pulse.message}
            </p>

        </Card>

    );

}