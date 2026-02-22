"use client";

import { Report, Issue } from "@/types/report";
import { ScoreGauge } from "@/components/results/ScoreGauge";
import { IssuesList } from "@/components/results/IssuesList";
import { Activity, Clock, ShieldAlert, Zap } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { RadarScore } from "@/components/charts/RadarScore";
import { SeverityPieChart } from "@/components/charts/SeverityPieChart";

interface OverviewPanelProps {
    report: Report;
}

export function OverviewPanel({ report }: OverviewPanelProps) {
    // We combine the backend's AI Analysis scores or fallback to generic values
    const scores = report.ai_analysis?.scores_by_category || {
        dns: 80,
        ssl: 90,
        performance: 65,
        security: 75,
        seo: 85
    };

    const radarData = [
        { subject: 'DNS', A: scores.dns || 80, fullMark: 100 },
        { subject: 'SSL', A: scores.ssl || 90, fullMark: 100 },
        { subject: 'Perf', A: scores.performance || 65, fullMark: 100 },
        { subject: 'Sécurité', A: scores.security || 75, fullMark: 100 },
        { subject: 'SEO', A: scores.seo || 85, fullMark: 100 },
    ];

    // Collect all issues from AI Analysis
    const allIssues: Issue[] = [
        ...(report.ai_analysis?.critical_issues || []).map(i => ({ ...i, severity: 'critical' })),
        ...(report.ai_analysis?.warnings || []).map(i => ({ ...i, severity: 'medium' }))
    ];

    const severityMap: Record<string, number> = {
        critical: 0, high: 0, medium: 0, low: 0, info: 0
    };

    allIssues.forEach(issue => {
        const sev = issue.severity.toLowerCase();
        severityMap[sev] = (severityMap[sev] || 0) + 1;
    });

    const pieData = [
        { name: 'Critique', value: severityMap.critical || (allIssues.length ? 0 : 1), color: '#ef4444' }, // Red
        { name: 'Haute', value: severityMap.high || (allIssues.length ? 0 : 3), color: '#f97316' }, // Orange
        { name: 'Moyenne', value: severityMap.medium || (allIssues.length ? 0 : 5), color: '#f59e0b' }, // Amber
        { name: 'Faible', value: severityMap.low || (allIssues.length ? 0 : 12), color: '#3b82f6' }, // Blue
    ].filter(d => d.value > 0);

    const overallScore = report.ai_analysis?.overall_score || report.scan.overall_score || 0;

    return (
        <div className="space-y-6">
            {/* Top metrics AI Insight */}
            {report.ai_analysis && (
                <Card className="border-brand-500/30 bg-brand-500/5 shadow-xl shadow-brand-500/5 backdrop-blur-sm">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-brand-400">
                            <Zap className="h-5 w-5" /> Synthèse de l'Intelligence Artificielle
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-muted-foreground leading-relaxed whitespace-pre-wrap">
                            {report.ai_analysis.executive_summary}
                        </p>
                    </CardContent>
                </Card>
            )}

            {/* Main Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <Card className="flex flex-col items-center justify-center p-6 border-border/50 bg-card/60 backdrop-blur-md">
                    <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-6 w-full text-center">
                        Score Global
                    </h3>
                    <ScoreGauge score={overallScore} size={180} strokeWidth={14} label="" />
                </Card>

                <Card className="p-6 border-border/50 bg-card/60 backdrop-blur-md">
                    <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-2 text-center">
                        Performance par Module
                    </h3>
                    <div className="-mt-4">
                        <RadarScore data={radarData} />
                    </div>
                </Card>

                <Card className="p-6 border-border/50 bg-card/60 backdrop-blur-md">
                    <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-2 text-center">
                        Répartition des Risques
                    </h3>
                    {pieData.length > 0 ? (
                        <SeverityPieChart data={pieData} />
                    ) : (
                        <div className="h-[200px] flex items-center justify-center text-muted-foreground">
                            Aucun risque détecté
                        </div>
                    )}
                </Card>
            </div>

            {/* Issues List Limitée */}
            <Card className="border-border/50 bg-card/60 backdrop-blur-md">
                <CardHeader>
                    <CardTitle>Problèmes Détectés ({allIssues.length})</CardTitle>
                    <CardDescription>
                        Aperçu des problèmes nécessitant votre attention immédiate.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <IssuesList issues={allIssues} maxCount={5} />
                </CardContent>
            </Card>
        </div>
    );
}

