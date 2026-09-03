import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import CashFlowCard from "../../components/dashboard/CashFlowCard";

describe("CashFlowCard", () => {

    it("renders the title and formats the amount as Indian rupees", () => {

        render(
            <CashFlowCard
                title="Income"
                amount={45000}
            />
        );

        expect(screen.getByText("Income")).toBeInTheDocument();
        expect(screen.getByText("₹45,000")).toBeInTheDocument();

    });

    it("does not render a trend line when no change is given", () => {

        // Regression test: Dashboard.jsx used to hardcode fake trend
        // percentages ("+12%" etc.) here regardless of real data. The
        // fix was to only render this line when a real value is
        // passed -- this locks that behavior in.
        const { container } = render(
            <CashFlowCard
                title="Savings"
                amount={12000}
            />
        );

        expect(container.querySelectorAll("p")).toHaveLength(1);

    });

    it("renders the trend line, colored green, when a positive change is given", () => {

        render(
            <CashFlowCard
                title="Income"
                amount={45000}
                change="+12%"
                positive
            />
        );

        const trend = screen.getByText("+12%");

        expect(trend).toBeInTheDocument();
        expect(trend.className).toContain("text-green-600");

    });

    it("renders the trend line, colored red, when positive is false", () => {

        render(
            <CashFlowCard
                title="Expenses"
                amount={8000}
                change="-8%"
                positive={false}
            />
        );

        const trend = screen.getByText("-8%");

        expect(trend.className).toContain("text-red-500");

    });

});
