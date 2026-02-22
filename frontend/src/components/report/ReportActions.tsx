"use client";

import { useReport } from "@/hooks/useReport";
import { Button } from "@/components/ui/button";
import { Download, Mail, Share2, Loader2 } from "lucide-react";
import { toast } from "sonner";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface ReportActionsProps {
    scanId: string;
}

export function ReportActions({ scanId }: ReportActionsProps) {
    const { downloadPdf, sendEmail, isDownloading, isEmailing } = useReport(scanId);

    const handleDownload = async () => {
        try {
            await downloadPdf();
            toast.success("Téléchargement du PDF démarré");
        } catch {
            toast.error("Échec du téléchargement");
        }
    };

    const handleEmail = async () => {
        try {
            await sendEmail("user@example.com"); // Normalement, on aurait un modal pour l'email
            toast.success("Rapport envoyé par email");
        } catch {
            toast.error("Échec de l'envoi de l'email");
        }
    };

    return (
        <div className="flex items-center gap-2">
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button variant="outline" className="h-10 border-border/50 bg-background/50 backdrop-blur-sm">
                        <Share2 className="mr-2 h-4 w-4" />
                        Partager
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={handleEmail} disabled={isEmailing} className="cursor-pointer">
                        {isEmailing ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Mail className="mr-2 h-4 w-4" />}
                        Envoyer par email
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>

            <Button
                onClick={handleDownload}
                disabled={isDownloading}
                className="h-10 bg-brand-500 hover:bg-brand-600 shadow-lg shadow-brand-500/20"
            >
                {isDownloading ? (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                    <Download className="mr-2 h-4 w-4" />
                )}
                Export PDF
            </Button>
        </div>
    );
}
