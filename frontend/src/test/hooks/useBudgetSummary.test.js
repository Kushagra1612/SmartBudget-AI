import { describe, it, expect, vi, beforeEach } from "vitest";
import { renderHook, waitFor, act } from "@testing-library/react";
import useBudgetSummary from "../../hooks/useBudgetSummary";
import { getBudgetSummary } from "../../api/budget";

vi.mock("../../api/budget", () => ({
    getBudgetSummary: vi.fn(),
}));

describe("useBudgetSummary", () => {

    beforeEach(() => {

        vi.clearAllMocks();

    });

    it("starts loading, then resolves with the fetched summary", async () => {

        getBudgetSummary.mockResolvedValue([
            { id: "1", category: "Food", spent: 400, monthly_limit: 1000 },
        ]);

        const { result } = renderHook(() => useBudgetSummary());

        expect(result.current.loading).toBe(true);
        expect(result.current.summary).toEqual([]);

        await waitFor(() => {
            expect(result.current.loading).toBe(false);
        });

        expect(result.current.summary).toEqual([
            { id: "1", category: "Food", spent: 400, monthly_limit: 1000 },
        ]);
        expect(result.current.error).toBe(null);
        expect(getBudgetSummary).toHaveBeenCalledTimes(1);

    });

    it("sets error and stops loading when the fetch fails", async () => {

        getBudgetSummary.mockRejectedValue(new Error("Network error"));

        const { result } = renderHook(() => useBudgetSummary());

        await waitFor(() => {
            expect(result.current.loading).toBe(false);
        });

        expect(result.current.error).toBeInstanceOf(Error);
        expect(result.current.summary).toEqual([]);

    });

    it("refetch() re-fetches and replaces the summary with fresh data", async () => {

        // Regression coverage: Budget.jsx used to hand-patch local state
        // after creating/updating a budget (and, worse, sometimes just
        // called window.location.reload()). The fix was to expose a
        // refetch() that pulls fresh data from the server instead --
        // this confirms calling it actually replaces stale data.
        getBudgetSummary.mockResolvedValueOnce([
            { id: "1", category: "Food", spent: 400, monthly_limit: 1000 },
        ]);

        const { result } = renderHook(() => useBudgetSummary());

        await waitFor(() => {
            expect(result.current.loading).toBe(false);
        });

        expect(result.current.summary).toHaveLength(1);

        getBudgetSummary.mockResolvedValueOnce([
            { id: "1", category: "Food", spent: 400, monthly_limit: 1000 },
            { id: "2", category: "Transport", spent: 200, monthly_limit: 500 },
        ]);

        await act(async () => {
            await result.current.refetch();
        });

        await waitFor(() => {
            expect(result.current.summary).toHaveLength(2);
        });

        expect(getBudgetSummary).toHaveBeenCalledTimes(2);

    });

});
