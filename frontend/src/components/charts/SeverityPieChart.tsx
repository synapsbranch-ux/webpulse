"use client";

import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

interface SeverityPieChartProps {
    data: {
        name: string;
        value: number;
        color: string;
    }[];
}

export function SeverityPieChart({ data }: SeverityPieChartProps) {
    const filteredData = data.filter(d => d.value > 0);

    if (filteredData.length === 0) {
        return (
            <div className="h-[250px] w-full flex items-center justify-center text-muted-foreground text-sm border-dashed border rounded-xl">
                Aucune donnée de sévérité
            </div>
        );
    }

    return (
        <div className="h-[250px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                    <Pie
                        data={filteredData}
                        cx="50%"
                        cy="45%"
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                        dataKey="value"
                    >
                        {filteredData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                    </Pie>
                    <Tooltip
                        contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                        itemStyle={{ color: '#fff' }}
                    />
                    <Legend verticalAlign="bottom" height={36} wrapperStyle={{ fontSize: '12px' }} />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
}
