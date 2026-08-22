import { useEffect, useState } from "react";
import { getPulse } from "../api/ai";

export default function useAIPulse() {

    const [pulse, setPulse] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        async function fetchPulse() {

            try {

                const data = await getPulse();

                setPulse(data);

            } catch (error) {

                console.error(error);

            } finally {

                setLoading(false);

            }

        }

        fetchPulse();

    }, []);

    return {
        pulse,
        loading,
    };

}