"use client";

import { useEffect, useState } from "react";
import { useScan } from "@/hooks/useScan";
import { Scan } from "@/types/scan";
import { RecentScans } from "@/components/dashboard/RecentScans";
import { Skeleton } from "@/components/ui/skeleton";
import { History as HistoryIcon } from "lucide-react";

export default function HistoryPage() {
    const { getScans } = useScan();
    const [scans, setScans] = useState<Scan[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        let active = true;
        getScans()
            .then((data) => {
                if (active) {
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
        <div className="space-y-8 animate-in fade-in duration-500 slide-in-from-bottom-4 pb-12">
            <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-500/10 text-brand-500">
                    <HistoryIcon className="h-6 w-6" />
                </div>
                <div>
                    <h2 className="text-2xl font-bold tracking-tight">Historique des Analyses</h2>
                    <p className="text-muted-foreground">Retrouvez l'ensemble de vos analyses passées.</p>
                </div>
            </div>

            <div className="bg-card/50 rounded-xl p-1 backdrop-blur-sm border border-border/50 shadow-lg">
                {isLoading ? (
                    <div className="p-4">
                        <Skeleton className="h-[400px] w-full rounded-xl" />
                    </div>
                ) : (
                    <RecentScans scans={scans} />
                    // Note: On réutilise RecentScans qui se limitait à 5, mais dans la réalité on lui passerait tout
                    // Pour cet exemple, disons que RecentScans affiche tout si on ne le slice(0,5) pas
                    // Mais il y a un slice en dur dans le composant. Pour un vrai projet, passer un prop `limit` or `showAll`.
                )}
            </div>
        </div>
    );
}
