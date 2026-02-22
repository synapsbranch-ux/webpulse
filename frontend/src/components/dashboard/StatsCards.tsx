"use client";

import { BarChart3, Target, AlertTriangle, Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Scan } from "@/types/scan";
import { formatScore } from "@/lib/utils";
import { formatDistanceToNow } from "date-fns";
import { fr } from "date-fns/locale";

interface StatsCardsProps {
    scans: Scan[];
}

export function StatsCards({ scans }: StatsCardsProps) {
    const completedScans = scans.filter(s => s.status === 'completed');
    const totalScans = scans.length;

    const avgScore = completedScans.length > 0
        ? completedScans.reduce((acc, s) => acc + (s.overall_score || 0), 0) / completedScans.length
        : 0;

    // Pseudo-logic for issues detected (would usually come from a deeper endpoint)
    const issuesDetected = completedScans.filter(s => (s.overall_score || 100) < 80).length;

    const lastScan = scans.length > 0 ? scans[0] : null;

    return (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-muted-foreground">Total Scans</CardTitle>
                    <BarChart3 className="h-4 w-4 text-brand-500" />
                </CardHeader>
                <CardContent>
                    <div className="text-2xl font-bold">{totalScans}</div>
                </CardContent>
            </Card>

            <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-muted-foreground">Score Moyen</CardTitle>
                    <Target className="h-4 w-4 text-emerald-500" />
                </CardHeader>
                <CardContent>
                    <div className="text-2xl font-bold">{formatScore(avgScore)}</div>
                </CardContent>
            </Card>

            <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-muted-foreground">Problèmes Fréquents</CardTitle>
                    <AlertTriangle className={`h-4 w-4 ${issuesDetected > 0 ? 'text-red-500' : 'text-emerald-500'}`} />
                </CardHeader>
                <CardContent>
                    <div className="text-2xl font-bold">{issuesDetected} sites à risque</div>
                </CardContent>
            </Card>

            <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-muted-foreground">Dernier Scan</CardTitle>
                    <Clock className="h-4 w-4 text-brand-400" />
                </CardHeader>
                <CardContent>
                    <div className="text-2xl font-bold truncate text-base mt-1">
                        {lastScan?.created_at
                            ? `Il y a ${formatDistanceToNow(new Date(lastScan.created_at), { locale: fr })}`
                            : "Aucun scan"}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
