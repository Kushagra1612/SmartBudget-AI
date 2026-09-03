import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen } from "@testing-library/react";
import ErrorBoundary from "../../components/common/ErrorBoundary";

function Bomb() {
    throw new Error("Boom");
}

describe("ErrorBoundary", () => {

    beforeEach(() => {

        // React logs the caught error to the console by default (twice,
        // in dev mode) -- expected and noisy, not a real test failure.
        // Silencing it keeps test output readable.
        vi.spyOn(console, "error").mockImplementation(() => {});

    });

    afterEach(() => {

        console.error.mockRestore();

    });

    it("renders children normally when nothing throws", () => {

        render(
            <ErrorBoundary>
                <p>Everything is fine</p>
            </ErrorBoundary>
        );

        expect(screen.getByText("Everything is fine")).toBeInTheDocument();

    });

    it("shows a recoverable fallback instead of crashing when a child throws", () => {

        render(
            <ErrorBoundary>
                <Bomb />
            </ErrorBoundary>
        );

        expect(screen.getByText("Something went wrong")).toBeInTheDocument();
        expect(screen.getByRole("button", { name: "Reload" })).toBeInTheDocument();

        // The thing that broke shouldn't still be on the page.
        expect(screen.queryByText("Everything is fine")).not.toBeInTheDocument();

    });

});
