import MainLayout from "../layouts/MainLayout";

import TransactionsHeader
from "../components/transactions/TransactionsHeader";

import TransactionFilters
from "../components/transactions/TransactionFilters";

export default function Transactions() {

    return (

        <MainLayout>

            <TransactionsHeader/>

            <TransactionFilters/>

        </MainLayout>

    );

}