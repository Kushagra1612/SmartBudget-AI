import { useEffect, useState } from "react";
import { getTransactions } from "../api/transactions";

export default function useTransactions() {

    const [transactions, setTransactions] = useState([]);

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        async function load() {

            try {

                const data = await getTransactions();

                setTransactions(data);

            } finally {

                setLoading(false);

            }

        }

        load();

    }, []);

    return {
        transactions,
        loading,
    };

}