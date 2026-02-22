"use client";

import { LiveMetrics as LiveMetricsType } from "@/types/scan";
import { MetricCard } from "@/components/results/MetricCard";
import { Activity, Clock, ServerCrash, Cpu } from "lucide-react";

interface LiveMetricsProps {
    metrics: LiveMetricsType | null;
    isLoading?: boolean;
}

export function LiveMetrics({ metrics, isLoading }: LiveMetricsProps) {
    const data = metrics || {
        avg_response_time: 0,
        throughput: 0,
        error_rate: 0,
        active_users: 0,
    };

    return (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <MetricCard
                title="Temps de Réponse"
                value={`${data.avg_response_time} ms`}
                icon={Clock}
                trend={{ value: 12, isPositive: false }} // Exemple
                isLoading={isLoading}
            />
            <MetricCard
                title="Débit (Req/s)"
                value={data.throughput}
                icon={Activity}
                trend={{ value: 5, isPositive: true }}
                isLoading={isLoading}
            />
            <MetricCard
                title="Taux d'Erreur"
                value={`${data.error_rate}%`}
                icon={ServerCrash}
                isLoading={isLoading}
            />
            <MetricCard
                title="Utilisateurs Actifs"
                value={data.active_users}
                icon={Cpu}
                isLoading={isLoading}
            />
        </div>
    );
}

