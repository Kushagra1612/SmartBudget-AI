import MainLayout from "../layouts/MainLayout";

import GreetingHeader from "../components/dashboard/GreetingHeader";
import DashboardGrid from "../components/dashboard/DashboardGrid";
import FinancialHealthCard from "../components/dashboard/FinancialHealthCard";
import CashFlowCard from "../components/dashboard/CashFlowCard";
import AIPulseCard from "../components/dashboard/AIPulseCard";
import GoalsPreview from "../components/dashboard/GoalsPreview";
import SpendingOverview from "../components/dashboard/SpendingOverview";
import RecentActivity from "../components/dashboard/RecentActivity";

import useDashboard from "../hooks/useDashboard";

export default function Dashboard() {

    const currentDate = new Date();

    const {
        dashboard,
        loading,
        error,
    } = useDashboard(
        currentDate.getMonth() + 1,
        currentDate.getFullYear(),
    );

    if (loading) {
    return (
        <MainLayout>
            <div className="p-10 text-center text-gray-500">
                Loading dashboard...
            </div>
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
    change="+12%"
/>

<CashFlowCard
    title="Expenses"
    amount={dashboard.monthly_expenses}
    change="-8%"
    positive={false}
/>

<CashFlowCard
    title="Savings"
    amount={dashboard.savings}
    change="+20%"
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
                    <RecentActivity
                         transactions={dashboard.recent_transactions}
                    />
                </div>

            </DashboardGrid>

        </MainLayout>

    );
}