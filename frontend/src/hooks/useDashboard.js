import { useEffect, useState } from "react";
import { getDashboard } from "../api/dashboard";

export default function useDashboard(month, year) {

    const [dashboard, setDashboard] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);

    useEffect(() => {

        async function fetchDashboard() {

            try {

                const data = await getDashboard(
                    month,
                    year,
                );

                setDashboard(data);

            } catch (err) {

                setError(err);

            } finally {

                setLoading(false);

            }

        }

        fetchDashboard();

    }, [month, year]);

    return {

        dashboard,

        loading,

        error,

    };

}