import { useCallback, useEffect, useState } from "react";
import { getStatements } from "../api/statements";

export default function useStatements() {

    const [statements, setStatements] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const refetch = useCallback(async () => {

        try {

            const data = await getStatements();

            setStatements(data);

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
        statements,
        loading,
        error,
        refetch,
    };

}