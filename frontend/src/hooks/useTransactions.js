import { useEffect, useState } from "react";
import { getTransactions } from "../api/transaction";

export default function useTransactions() {

    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {

        async function fetchTransactions() {

            try {

                const data = await getTransactions();

                setTransactions(data);

            } catch (err) {

                setError(err);

            } finally {

                setLoading(false);

            }

        }

        fetchTransactions();

    }, []);

    return {
        transactions,
        loading,
        error,
    };

}