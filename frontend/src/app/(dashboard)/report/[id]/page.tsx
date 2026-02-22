"use client";

import { use, useEffect, useState } from "react";
import { useReport } from "@/hooks/useReport";
import { Report } from "@/types/report";
import { ReportViewer } from "@/components/report/ReportViewer";
import { ReportActions } from "@/components/report/ReportActions";
import { Skeleton } from "@/components/ui/skeleton";
import { AlertCircle, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { formatDate } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

export default function ReportPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = use(params);
    const router = useRouter();
    const { getReport, isLoading, error } = useReport(id);
    const [report, setReport] = useState<Report | null>(null);

    useEffect(() => {
        let active = true;
        getReport()
            .then(data => {
                if (active) setReport(data);
            })
            .catch(() => { });
        return () => { active = false; };
    }, [getReport]);

    if (isLoading) {
        return (
            <div className="space-y-8 animate-in fade-in">
                <div className="flex justify-between items-start">
                    <div className="space-y-2">
                        <Skeleton className="h-10 w-64" />
                        <Skeleton className="h-5 w-48" />
                    </div>
                    <Skeleton className="h-10 w-32" />
                </div>
                <Skeleton className="h-16 w-full" />
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Skeleton className="h-64" />
                    <Skeleton className="h-64" />
                    <Skeleton className="h-64" />
                </div>
            </div>
        );
    }

    if (error || !report) {
        return (
            <div className="flex flex-col items-center justify-center py-20 text-center">
                <AlertCircle className="h-16 w-16 text-red-500 mb-6" />
                <h2 className="text-2xl font-bold mb-2">Rapport Introuvable</h2>
                <p className="text-muted-foreground max-w-md mx-auto mb-8">
                    Le rapport demandé n'existe pas ou n'a pas pu être chargé. Assurez-vous que le scan est bien terminé.
                </p>
                <Button onClick={() => router.push('/dashboard')}>
                    Retour au Dashboard
                </Button>
            </div>
        );
    }

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-12">
            <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                <div>
                    <Button
                        variant="ghost"
                        size="sm"
                        className="-ml-3 mb-2 text-muted-foreground hover:text-foreground"
                        onClick={() => router.back()}
                    >
                        <ArrowLeft className="mr-2 h-4 w-4" /> Retour
                    </Button>
                    <div className="flex items-center gap-3 mb-2">
                        <h1 className="text-3xl font-bold tracking-tight">Rapport d'Analyse</h1>
                        <Badge variant="outline" className="bg-brand-500/10 text-brand-500 border-none font-semibold">
                            Finalisé
                        </Badge>
                    </div>
                    <p className="text-muted-foreground flex items-center gap-2">
                        Cible: <span className="font-semibold text-foreground">{report.scan.url}</span>
                        <span className="text-border px-2">|</span>
                        Généré le: {formatDate(report.created_at)}
                    </p>
                </div>

                <ReportActions scanId={id} />
            </div>

            <div className="pt-2">
                <ReportViewer report={report} />
            </div>
        </div>
    );
}
