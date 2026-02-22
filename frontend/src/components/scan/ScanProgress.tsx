"use client";

import { Progress } from "@/components/ui/progress";
import { PHASES } from "@/lib/constants";

interface ScanProgressProps {
    currentPhase: string;
    overallProgress?: number; // Force un pourcentage si fourni
}

export function ScanProgress({ currentPhase, overallProgress }: ScanProgressProps) {
    const calculateProgress = () => {
        if (overallProgress !== undefined) return overallProgress;

        if (currentPhase === 'completed') return 100;

        const currentIndex = PHASES.findIndex((p: any) => p.id === currentPhase);
        if (currentIndex === -1) return 0;

        // Si on a 6 phases, on calcule la progression de base
        // Ex: phase 0 -> 10%, phase 5 -> 90% (jamais 100% avant "completed")
        const step = 90 / PHASES.length;
        return Math.floor(10 + currentIndex * step);
    };

    const progress = calculateProgress();

    return (
        <div className="w-full space-y-2">
            <div className="flex justify-between items-center text-sm font-medium">
                <span className="text-muted-foreground">Progression Globale</span>
                <span className="text-brand-500">{progress}%</span>
            </div>
            <Progress value={progress} className="h-2 bg-muted">
                <div
                    className="h-full bg-brand-500 transition-all duration-500 ease-in-out"
                    style={{ width: `${progress}%` }}
                />
            </Progress>
        </div>
    );
}

