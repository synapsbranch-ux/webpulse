"use client";

import { useMemo } from "react";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import { LiveMetrics } from "@/types/scan";

interface LiveLineChartProps {
    dataStream?: LiveMetrics[];
    dataKey: keyof LiveMetrics;
    color?: string;
    name?: string;
}

export function LiveLineChart({ dataStream = [], dataKey, color = "#3b82f6", name = "Valeur" }: LiveLineChartProps) {
    // Garder seulement les X derniers points ou créer un dummy
    const displayData = useMemo(() => {
        if (dataStream.length === 0) {
            return Array.from({ length: 20 }, (_, i) => ({ time: i, [dataKey]: 0 }));
        }
        return dataStream.slice(-30).map((d, i) => ({
            time: i,
            [dataKey]: d[dataKey]
        }));
    }, [dataStream, dataKey]);

    return (
        <div className="h-[200px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={displayData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                    <XAxis dataKey="time" hide />
                    <YAxis
                        stroke="rgba(255,255,255,0.5)"
                        fontSize={12}
                        tickLine={false}
                        axisLine={false}
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                        formatter={(value: any) => [`${value}`, name]}
                        labelFormatter={() => ''}
                    />
                    <Line
                        type="monotone"
                        dataKey={dataKey as string}
                        stroke={color}
                        strokeWidth={2}
                        dot={false}
                        isAnimationActive={false} // Désactiver l'animation Recharts pour les flux rapides
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
