import { useEffect, useState } from "react";
import { getDailyPulse } from "../api/ai";

export default function useAIPulse() {

    const [pulse, setPulse] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        async function fetchPulse() {

            try {

                const currentDate = new Date();

                const data = await getDailyPulse(
                    currentDate.getMonth() + 1,
                    currentDate.getFullYear(),
                );

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