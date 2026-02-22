"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Scan } from "@/types/scan";
import { formatScore, getGradeColor, formatDate } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Eye, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

interface RecentScansProps {
    scans: Scan[];
}

export function RecentScans({ scans }: RecentScansProps) {
    const router = useRouter();
    const recent = scans.slice(0, 5);

    const getStatusBadge = (status: string) => {
        switch (status) {
            case 'completed': return <Badge variant="default" className="bg-emerald-500/10 text-emerald-500 border-none">Terminé</Badge>;
            case 'failed': return <Badge variant="destructive" className="bg-red-500/10 text-red-500 border-none">Échoué</Badge>;
            case 'running': return <Badge variant="secondary" className="bg-blue-500/10 text-blue-500 border-none animate-pulse">En cours</Badge>;
            default: return <Badge variant="outline" className="text-muted-foreground">En attente</Badge>;
        }
    };

    if (recent.length === 0) {
        return (
            <div className="text-center py-12 border rounded-xl border-dashed">
                <p className="text-muted-foreground">Aucun scan récent. Lancez votre première analyse !</p>
            </div>
        );
    }

    return (
        <div className="rounded-xl border border-border/50 bg-card/50 backdrop-blur-sm overflow-hidden">
            <Table>
                <TableHeader className="bg-muted/50">
                    <TableRow>
                        <TableHead>URL</TableHead>
                        <TableHead>Score</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Date</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {recent.map((scan) => {
                        const gradeLetter = scan.overall_score !== undefined
                            ? (scan.overall_score >= 90 ? 'A' : scan.overall_score >= 80 ? 'B' : scan.overall_score >= 70 ? 'C' : scan.overall_score >= 60 ? 'D' : 'F')
                            : undefined;

                        return (
                            <TableRow key={scan.id} className="hover:bg-muted/30 transition-colors">
                                <TableCell className="font-medium">
                                    <div className="truncate max-w-[250px]" title={scan.url}>
                                        {scan.url}
                                    </div>
                                </TableCell>
                                <TableCell>
                                    {scan.status === 'completed' && scan.overall_score !== undefined ? (
                                        <Badge variant="outline" className={getGradeColor(gradeLetter)}>
                                            {formatScore(scan.overall_score)}
                                        </Badge>
                                    ) : (
                                        <span className="text-muted-foreground">-</span>
                                    )}
                                </TableCell>
                                <TableCell>{getStatusBadge(scan.status)}</TableCell>
                                <TableCell className="text-muted-foreground whitespace-nowrap">
                                    {formatDate(scan.created_at)}
                                </TableCell>
                                <TableCell className="text-right">
                                    <div className="flex justify-end gap-2">
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            onClick={() => router.push(`/scan/${scan.id}`)}
                                            title="Voir les résultats"
                                        >
                                            <Eye className="h-4 w-4" />
                                        </Button>
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            className="text-red-500 hover:text-red-600 hover:bg-red-500/10"
                                            onClick={() => alert('À implémenter: Suppression')}
                                            title="Supprimer"
                                        >
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </TableCell>
                            </TableRow>
                        );
                    })}
                </TableBody>
            </Table>
        </div>
    );
}
