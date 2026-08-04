import {
    ArrowDownLeft,
    ArrowUpRight,
    ShoppingBag,
    Utensils,
} from "lucide-react";

import Card from "../common/Card";

const activities = [
    {
        icon: ArrowDownLeft,
        title: "Salary Credited",
        amount: "+ ₹55,000",
        color: "text-green-600",
    },
    {
        icon: ShoppingBag,
        title: "Amazon Purchase",
        amount: "- ₹2,100",
        color: "text-red-500",
    },
    {
        icon: Utensils,
        title: "Burger King",
        amount: "- ₹420",
        color: "text-red-500",
    },
    {
        icon: ArrowUpRight,
        title: "Savings Transfer",
        amount: "+ ₹8,000",
        color: "text-green-600",
    },
];

export default function RecentActivity() {

    return (

        <Card>

            <h2 className="text-2xl font-bold">

                Recent Activity

            </h2>

            <p className="text-gray-500 mt-1">

                Latest transactions

            </p>

            <div className="mt-8 space-y-6">

                {activities.map((item, index) => {

                    const Icon = item.icon;

                    return (

                        <div
                            key={index}
                            className="flex justify-between items-center"
                        >

                            <div className="flex items-center gap-4">

                                <div className="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center">

                                    <Icon size={20} />

                                </div>

                                <span className="font-medium">

                                    {item.title}

                                </span>

                            </div>

                            <span
                                className={`font-bold ${item.color}`}
                            >
                                {item.amount}
                            </span>

                        </div>

                    );

                })}

            </div>

        </Card>

    );

}