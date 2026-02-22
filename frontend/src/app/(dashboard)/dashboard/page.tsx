"use client";

import { useEffect, useState } from "react";
import { useScan } from "@/hooks/useScan";
import { Scan } from "@/types/scan";
import { StatsCards } from "@/components/dashboard/StatsCards";
import { QuickScan } from "@/components/dashboard/QuickScan";
import { RecentScans } from "@/components/dashboard/RecentScans";
import { Skeleton } from "@/components/ui/skeleton";

export default function DashboardPage() {
    const { getScans } = useScan();
    const [scans, setScans] = useState<Scan[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        let active = true;
        getScans()
            .then((data) => {
                if (active) {
                    // Sort by newest first
                    const sorted = data.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
                    setScans(sorted);
                }
            })
            .catch(() => { })
            .finally(() => {
                if (active) setIsLoading(false);
            });

        return () => { active = false; };
    }, [getScans]);

    return (
        <div className="space-y-8 animate-in fade-in duration-500 slide-in-from-bottom-4">
            <div>
                <h2 className="text-2xl font-bold tracking-tight">Vue d'ensemble</h2>
                <p className="text-muted-foreground">Bienvenue ! Voici l'état actuel de vos analyses.</p>
            </div>

            {isLoading ? (
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                    {[1, 2, 3, 4].map((i) => (
                        <Skeleton key={i} className="h-28 rounded-xl" />
                    ))}
                </div>
            ) : (
                <StatsCards scans={scans} />
            )}

            <QuickScan />

            <div className="space-y-4">
                <h3 className="text-xl font-semibold tracking-tight">Scans Récents</h3>
                {isLoading ? (
                    <Skeleton className="h-[300px] w-full rounded-xl" />
                ) : (
                    <RecentScans scans={scans} />
                )}
            </div>
        </div>
    );
}
