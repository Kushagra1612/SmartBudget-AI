import MainLayout from "../layouts/MainLayout";

import GreetingHeader from "../components/dashboard/GreetingHeader";
import DashboardGrid from "../components/dashboard/DashboardGrid";
import FinancialHealthCard from "../components/dashboard/FinancialHealthCard";
import CashFlowCard from "../components/dashboard/CashFlowCard";
import AIPulseCard from "../components/dashboard/AIPulseCard";
import GoalsPreview from "../components/dashboard/GoalsPreview";
import SpendingOverview from "../components/dashboard/SpendingOverview";
import RecentActivity from "../components/dashboard/RecentActivity";

export default function Dashboard() {

    return (

        <MainLayout>

            <GreetingHeader />
<DashboardGrid>

    <div className="col-span-4">

        <FinancialHealthCard />

    </div>

    <div className="col-span-8 grid grid-cols-3 gap-6">

        <CashFlowCard
            title="Income"
            amount="55,000"
            change="+12%"
        />

        <CashFlowCard
            title="Expenses"
            amount="31,000"
            change="-8%"
            positive={false}
        />

        <CashFlowCard
            title="Savings"
            amount="24,000"
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

    <SpendingOverview />

</div>

<div className="col-span-12">

    <RecentActivity />

</div>

</DashboardGrid>

        </MainLayout>

    );

}