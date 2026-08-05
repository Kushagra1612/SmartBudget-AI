import { useEffect, useState } from "react";
import { getBudgets } from "../api/budget";

export default function useBudget() {

    const currentDate = new Date();

    const [budgets, setBudgets] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        async function fetchBudgets() {

            try {

                const data = await getBudgets(
                    currentDate.getMonth() + 1,
                    currentDate.getFullYear(),
                );

                setBudgets(data);

            } catch (err) {

                console.error(err);

            } finally {

                setLoading(false);

            }

        }

        fetchBudgets();

    }, []);

    return {
        budgets,
        loading,
    };

}