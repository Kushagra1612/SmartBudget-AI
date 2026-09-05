import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import Card from "../common/Card";

const CHART_COLORS = [
    "var(--primary)",
    "var(--accent)",
    "var(--success)",
    "var(--warning)",
    "var(--danger)",
    "#8B5CF6",
    "#EC4899",
    "#06B6D4",
];

function formatRupees(value) {
    return `₹${Number(value).toLocaleString("en-IN", {
        maximumFractionDigits: 0,
    })}`;
}

export default function SpendingOverview({
    categories = [],
}) {

    const chartData = categories.map((item) => ({
        name: item.category,
        value: Number(item.amount),
    }));

    return (

        <Card>

            <h2 className="text-2xl font-bold">

                Spending Overview

            </h2>

            <p className="text-gray-500 mt-1">

                Top spending categories

            </p>

            {categories.length === 0 ? (

                <p className="text-gray-400 mt-8">

                    No spending data available.

                </p>

            ) : (

                <div className="mt-8 flex flex-col md:flex-row gap-8 items-center">

                    <div className="w-44 h-44 shrink-0">

                        <ResponsiveContainer width="100%" height="100%">

                            <PieChart>

                                <Pie
                                    data={chartData}
                                    dataKey="value"
                                    nameKey="name"
                                    innerRadius={50}
                                    outerRadius={80}
                                    paddingAngle={2}
                                >

                                    {chartData.map((entry, index) => (
                                        <Cell
                                            key={entry.name}
                                            fill={
                                                CHART_COLORS[
                                                    index % CHART_COLORS.length
                                                ]
                                            }
                                        />
                                    ))}

                                </Pie>

                                <Tooltip
                                    formatter={(value) => formatRupees(value)}
                                />

                            </PieChart>

                        </ResponsiveContainer>

                    </div>

                    <div className="flex-1 w-full space-y-6">

                        {categories.map((item, index) => (

                            <div key={item.category}>

                                <div className="flex justify-between mb-2">

                                    <span className="font-medium flex items-center gap-2">

                                        <span
                                            className="w-2.5 h-2.5 rounded-full shrink-0"
                                            style={{
                                                backgroundColor:
                                                    CHART_COLORS[
                                                        index %
                                                            CHART_COLORS.length
                                                    ],
                                            }}
                                        />

                                        {item.category}

                                    </span>

                                    <span className="font-semibold">

                                        {formatRupees(item.amount)}

                                    </span>

                                </div>

                                <div className="h-3 rounded-full bg-gray-200">

                                    <div
                                        className="h-full rounded-full"
                                        style={{
                                            width: `${item.percentage}%`,
                                            backgroundColor:
                                                CHART_COLORS[
                                                    index % CHART_COLORS.length
                                                ],
                                        }}
                                    />

                                </div>

                            </div>

                        ))}

                    </div>

                </div>

            )}

        </Card>

    );

}