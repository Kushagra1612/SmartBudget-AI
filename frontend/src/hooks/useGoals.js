import { useEffect, useState } from "react";
import { getGoals } from "../api/goals";

export default function useGoals() {

    const [goals, setGoals] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {

        async function fetchGoals() {

            try {

                const data = await getGoals();

                setGoals(data);

            } catch (err) {

                setError(err);

            } finally {

                setLoading(false);

            }

        }

        fetchGoals();

    }, []);

    return {
        goals,
        loading,
        error,
    };

}