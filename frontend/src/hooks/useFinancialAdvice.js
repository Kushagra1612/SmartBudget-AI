import { useEffect, useState } from "react";
import { getAdvice } from "../api/ai";

export default function useFinancialAdvice() {

    const [advice, setAdvice] = useState("");
    const [agentsUsed, setAgentsUsed] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        async function fetchAdvice() {

            try {

                const data = await getAdvice();

                setAdvice(data.advice);
                setAgentsUsed(data.agents_used);

            } finally {

                setLoading(false);

            }

        }

        fetchAdvice();

    }, []);

    return {
        advice,
        agentsUsed,
        loading,
    };

}