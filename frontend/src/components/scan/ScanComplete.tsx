"use client";

import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { ScoreGauge } from "@/components/results/ScoreGauge";
import { Button } from "@/components/ui/button";
import { FileText, ArrowRight, CheckCircle2 } from "lucide-react";
import { Scan } from "@/types/scan";

interface ScanCompleteProps {
    scan: Scan;
}

export function ScanComplete({ scan }: ScanCompleteProps) {
    const router = useRouter();

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="p-8 rounded-2xl border border-brand-500/30 bg-card/60 backdrop-blur-md shadow-2xl shadow-brand-500/10 text-center relative overflow-hidden"
        >
            {/* Decorative success background glow */}
            <div className="absolute inset-x-0 top-0 h-32 bg-gradient-to-b from-brand-500/10 to-transparent pointer-events-none" />

            <div className="relative z-10 flex flex-col items-center">
                <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-emerald-500/10 text-emerald-500 ring-8 ring-emerald-500/5">
                    <CheckCircle2 className="h-8 w-8" />
                </div>

                <h2 className="text-3xl font-bold tracking-tight mb-2">Analyse Terminée !</h2>
                <p className="text-muted-foreground mb-8 max-w-md mx-auto">
                    Nos robots ont exploré votre infrastructure de fond en comble. Voici un aperçu rapide de l'état de santé.
                </p>

                <div className="mb-10 p-6 rounded-2xl bg-background/50 border border-border/50 inline-block shadow-inner">
                    <ScoreGauge score={scan.overall_score || 0} size={160} strokeWidth={10} />
                </div>

                <div className="flex flex-col sm:flex-row gap-4 justify-center w-full max-w-md">
                    <Button
                        className="w-full flex-1"
                        variant="outline"
                        onClick={() => router.push('/dashboard')}
                    >
                        Retour au Dashboard
                    </Button>
                    <Button
                        className="w-full flex-1 bg-brand-500 hover:bg-brand-600 shadow-lg shadow-brand-500/20"
                        onClick={() => router.push(`/report/${scan.id}`)}
                    >
                        <FileText className="mr-2 h-4 w-4" />
                        Rapport IA Complet
                        <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                </div>
            </div>
        </motion.div>
    );
}
