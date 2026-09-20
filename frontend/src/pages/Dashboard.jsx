import MainLayout from "../layouts/MainLayout";

import GreetingHeader from "../components/dashboard/GreetingHeader";
import DashboardGrid from "../components/dashboard/DashboardGrid";
import DashboardSkeleton from "../components/dashboard/DashboardSkeleton";
import FinancialHealthCard from "../components/dashboard/FinancialHealthCard";
import CashFlowCard from "../components/dashboard/CashFlowCard";
import AIPulseCard from "../components/dashboard/AIPulseCard";
import GoalsPreview from "../components/dashboard/GoalsPreview";
import SpendingOverview from "../components/dashboard/SpendingOverview";
import BudgetOverviewCard from "../components/dashboard/BudgetOverviewCard";
import AnomalyAlerts from "../components/dashboard/AnomalyAlerts";
import RecentActivity from "../components/dashboard/RecentActivity";

import useDashboard from "../hooks/useDashboard";

function formatTrend(percentage) {

    if (percentage === null || percentage === undefined) {
        return undefined;
    }

    const sign = percentage >= 0 ? "+" : "";

    return `${sign}${percentage}% vs last month`;

}

export default function Dashboard() {

    const {
        dashboard,
        loading,
        error,
    } = useDashboard();

    if (loading) {
        return (
            <MainLayout>
                <GreetingHeader />
                <DashboardSkeleton />
            </MainLayout>
        );
    }

    if (error) {
        return (
            <MainLayout>
                <div className="p-10 text-center text-red-500">
                    Error loading dashboard.
                </div>
            </MainLayout>
        );
    }

    return (

        <MainLayout>

            <GreetingHeader />

            <DashboardGrid>

                <div className="col-span-4">
                    <FinancialHealthCard
                        score={dashboard.analytics.financial_score.score}
                        grade={dashboard.analytics.financial_score.grade}
                        status={dashboard.analytics.financial_score.status}
                    />

                </div>

                <div className="col-span-8 grid grid-cols-3 gap-6">

                    <CashFlowCard
                        title="Income"
                        amount={dashboard.monthly_income}
                        change={formatTrend(dashboard.income_change_percentage)}
                    />

                    <CashFlowCard
                        title="Expenses"
                        amount={dashboard.monthly_expenses}
                        change={formatTrend(dashboard.expenses_change_percentage)}
                        positive={false}
                    />

                    <CashFlowCard
                        title="Savings"
                        amount={dashboard.savings}
                        change={formatTrend(dashboard.savings_change_percentage)}
                    />

                    <div className="col-span-3">
                        <AIPulseCard />
                    </div>

                </div>

                <div className="col-span-5">
                    <GoalsPreview />
                </div>

                <div className="col-span-7">
                   <SpendingOverview
                        categories={dashboard.analytics.spending.categories}
                   />
                </div>

                <div className="col-span-12">
                    <BudgetOverviewCard />
                </div>

                <div className="col-span-12">
                    <AnomalyAlerts />
                </div>

                <div className="col-span-12">
                    <RecentActivity
                         transactions={dashboard.recent_transactions}
                    />
                </div>

            </DashboardGrid>

        </MainLayout>

    );
}