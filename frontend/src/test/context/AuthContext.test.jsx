import { describe, it, expect, vi, beforeEach } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { AuthProvider, useAuth } from "../../context/AuthContext";
import { getProfile } from "../../api/auth";

vi.mock("../../api/auth", () => ({
    getProfile: vi.fn(),
}));

function wrapper({ children }) {
    return <AuthProvider>{children}</AuthProvider>;
}

describe("AuthContext", () => {

    beforeEach(() => {

        vi.clearAllMocks();
        localStorage.clear();

    });

    it("stops loading with no user when there's no token in localStorage", async () => {

        const { result } = renderHook(() => useAuth(), { wrapper });

        await waitFor(() => {
            expect(result.current.loading).toBe(false);
        });

        expect(result.current.user).toBe(null);
        expect(getProfile).not.toHaveBeenCalled();

    });

    it("fetches and sets the user when a token exists (e.g. after a page refresh)", async () => {

        localStorage.setItem("access_token", "a-fake-token");

        getProfile.mockResolvedValue({
            data: { id: "1", full_name: "Ada Lovelace", email: "ada@example.com" },
        });

        const { result } = renderHook(() => useAuth(), { wrapper });

        await waitFor(() => {
            expect(result.current.loading).toBe(false);
        });

        expect(getProfile).toHaveBeenCalledTimes(1);
        expect(result.current.user).toEqual({
            id: "1",
            full_name: "Ada Lovelace",
            email: "ada@example.com",
        });

    });

    it("stops loading with no user when the stored token is invalid/expired", async () => {

        // The axios response interceptor is what actually clears storage
        // and redirects on a 401 -- this context just needs to not
        // crash and to leave the user unset.
        localStorage.setItem("access_token", "an-expired-token");

        getProfile.mockRejectedValue(new Error("401"));

        const { result } = renderHook(() => useAuth(), { wrapper });

        await waitFor(() => {
            expect(result.current.loading).toBe(false);
        });

        expect(result.current.user).toBe(null);

    });

});
