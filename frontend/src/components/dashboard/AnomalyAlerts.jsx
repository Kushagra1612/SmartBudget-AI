import Card from "../common/Card";
import useAnomalies from "../../hooks/useAnomalies";

export default function AnomalyAlerts() {

    const {
        anomalies,
        totalAnalyzed,
        insufficientData,
        message,
        loading,
        error,
    } = useAnomalies();

    if (loading) {
        return (
            <Card>
                Checking for unusual spending...
            </Card>
        );
    }

    if (error) {
        return (
            <Card>
                Unable to load spending alerts.
            </Card>
        );
    }

    return (

        <Card>

            <div className="flex justify-between items-center">

                <h2 className="text-2xl font-bold">
                    Spending Alerts
                </h2>

                {!insufficientData && (

                    <span className="text-sm text-gray-400">
                        {totalAnalyzed} transactions scanned
                    </span>

                )}

            </div>

            <div className="mt-6 space-y-4">

                {insufficientData && (

                    <p className="text-gray-500">
                        {message}
                    </p>

                )}

                {!insufficientData && anomalies.length === 0 && (

                    <p className="text-gray-500">
                        Nothing unusual in your recent spending.
                    </p>

                )}

                {!insufficientData && anomalies.length > 0 && (

                    anomalies.map((anomaly) => (

                        <div
                            key={anomaly.id}
                            className="flex justify-between items-start border-b pb-4 last:border-b-0 last:pb-0"
                        >

                            <div className="pr-4">

                                <p className="text-sm text-gray-500">
                                    {anomaly.reason}
                                </p>

                            </div>

                            <div className="text-right shrink-0">

                                <p className="font-bold text-red-500">
                                    ₹{Number(anomaly.amount).toLocaleString("en-IN")}
                                </p>

                                <span
                                    className="
                                        inline-block
                                        mt-1
                                        text-xs
                                        font-semibold
                                        text-red-600
                                        bg-red-50
                                        rounded-full
                                        px-2
                                        py-0.5
                                    "
                                >
                                    {Number(anomaly.confidence_score).toFixed(0)}% unusual
                                </span>

                            </div>

                        </div>

                    ))

                )}

            </div>

        </Card>

    );

}
