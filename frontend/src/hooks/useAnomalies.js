import { useEffect, useState } from "react";
import { getAnomalies } from "../api/anomaly";

export default function useAnomalies() {

    const [anomalies, setAnomalies] = useState([]);
    const [totalAnalyzed, setTotalAnalyzed] = useState(0);
    const [insufficientData, setInsufficientData] = useState(false);
    const [message, setMessage] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {

        async function fetchAnomalies() {

            try {

                const data = await getAnomalies();

                setAnomalies(data.anomalies);
                setTotalAnalyzed(data.total_transactions_analyzed);
                setInsufficientData(data.insufficient_data);
                setMessage(data.message);

            } catch (err) {

                setError(err);

            } finally {

                setLoading(false);

            }

        }

        fetchAnomalies();

    }, []);

    return {
        anomalies,
        totalAnalyzed,
        insufficientData,
        message,
        loading,
        error,
    };

}
