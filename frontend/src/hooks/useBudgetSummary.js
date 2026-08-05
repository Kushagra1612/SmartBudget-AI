import { useEffect, useState } from "react";
import { getBudgetSummary } from "../api/budget";

export default function useBudgetSummary() {

    const currentDate = new Date();

    const [summary, setSummary] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {

        async function fetchSummary() {

            try {

                const data = await getBudgetSummary(
                    currentDate.getMonth() + 1,
                    currentDate.getFullYear(),
                );

                setSummary(data);

            } catch (err) {

                setError(err);

            } finally {

                setLoading(false);

            }

        }

        fetchSummary();

    }, []);

    return {
        summary,
        loading,
        error,
    };

}