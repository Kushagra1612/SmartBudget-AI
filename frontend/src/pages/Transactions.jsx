import { useState } from "react";

import MainLayout from "../layouts/MainLayout";

import TransactionsHeader from "../components/transactions/TransactionsHeader";
import TransactionFilters from "../components/transactions/TransactionFilters";
import TransactionList from "../components/transactions/TransactionList";

export default function Transactions() {

    const [search, setSearch] = useState("");
    const [category, setCategory] = useState("");
    const [type, setType] = useState("");
    const [dateFrom, setDateFrom] = useState("");
    const [dateTo, setDateTo] = useState("");

    return (

        <MainLayout>

            <TransactionsHeader />

            <TransactionFilters
                search={search}
                setSearch={setSearch}
                category={category}
                setCategory={setCategory}
                type={type}
                setType={setType}
                dateFrom={dateFrom}
                setDateFrom={setDateFrom}
                dateTo={dateTo}
                setDateTo={setDateTo}
            />

            <TransactionList
                search={search}
                category={category}
                type={type}
                dateFrom={dateFrom}
                dateTo={dateTo}
            />

        </MainLayout>

    );

}