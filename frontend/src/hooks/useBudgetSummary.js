import { useCallback, useEffect, useState } from "react";
import { getBudgetSummary } from "../api/budget";

export default function useBudgetSummary() {

    const [summary, setSummary] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const refetch = useCallback(async () => {

        try {

            const data = await getBudgetSummary();

            setSummary(data);

        } catch (err) {

            setError(err);

        } finally {

            setLoading(false);

        }

    }, []);

    useEffect(() => {

        refetch();

    }, [refetch]);

    return {
        summary,
        loading,
        error,
        refetch,
    };

}