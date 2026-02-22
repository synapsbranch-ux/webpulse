"use client";

import { Issue } from "@/types/report";
import { AlertTriangle, AlertCircle, Info, ChevronRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";

interface IssuesListProps {
    issues: Issue[];
    maxCount?: number;
}

export function IssuesList({ issues, maxCount }: IssuesListProps) {
    const displayIssues = maxCount ? issues.slice(0, maxCount) : issues;

    const getSeverityData = (severity: string) => {
        switch (severity) {
            case 'critical':
            case 'high':
                return { icon: AlertCircle, color: 'text-red-500', bg: 'bg-red-500/10 border-red-500/20' };
            case 'medium':
                return { icon: AlertTriangle, color: 'text-amber-500', bg: 'bg-amber-500/10 border-amber-500/20' };
            case 'low':
            case 'info':
            default:
                return { icon: Info, color: 'text-blue-500', bg: 'bg-blue-500/10 border-blue-500/20' };
        }
    };

    if (issues.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center p-8 text-center border rounded-xl border-dashed">
                <div className="h-12 w-12 rounded-full bg-emerald-500/10 flex items-center justify-center mb-3">
                    <Check className="h-6 w-6 text-emerald-500" />
                </div>
                <p className="font-medium text-emerald-500">Aucun problème détecté</p>
                <p className="text-sm text-muted-foreground mt-1">Excellent travail ! Votre site est en parfaite santé.</p>
            </div>
        );
    }

    return (
        <ScrollArea className="h-[400px] pr-4">
            <div className="space-y-4">
                {displayIssues.map((issue, idx) => {
                    const { icon: Icon, color, bg } = getSeverityData(issue.severity);
                    return (
                        <div key={idx} className="group flex gap-4 p-4 rounded-xl border border-border/50 bg-card hover:bg-muted/50 transition-colors">
                            <div className={`mt-0.5 shrink-0 flex h-8 w-8 items-center justify-center rounded-full border ${bg}`}>
                                <Icon className={`h-4 w-4 ${color}`} />
                            </div>
                            <div className="flex-1 space-y-1">
                                <div className="flex items-start justify-between gap-4">
                                    <h4 className="font-medium leading-tight">{issue.title}</h4>
                                    <Badge variant="outline" className={`uppercase tracking-wider text-[10px] font-bold ${color} ${bg}`}>
                                        {issue.severity}
                                    </Badge>
                                </div>
                                <p className="text-sm text-muted-foreground line-clamp-2 leading-relaxed">
                                    {issue.description}
                                </p>
                                <div className="flex items-center gap-2 pt-2 text-xs font-medium text-brand-500 cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity">
                                    Voir les détails <ChevronRight className="h-3 w-3" />
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </ScrollArea>
    );
}

// Composant interne pour l'icône de succès
function Check({ className }: { className?: string }) {
    return (
        <svg className={className} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12" />
        </svg>
    );
}
