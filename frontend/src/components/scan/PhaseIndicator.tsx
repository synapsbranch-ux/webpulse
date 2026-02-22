"use client";

import { Check, CircleDashed, Loader2 } from "lucide-react";
import { PHASES } from "@/lib/constants";
import { cn } from "@/lib/utils";

interface PhaseIndicatorProps {
    currentPhase: string;
}

export function PhaseIndicator({ currentPhase }: PhaseIndicatorProps) {
    // Déterminer l'index actuel
    const currentIndex = PHASES.findIndex((p: any) => p.id === currentPhase);
    // Si -1, c'est probablement terminé ou initié avec un ID inconnu
    const activeIndex = currentIndex === -1 && currentPhase === 'completed' ? PHASES.length : currentIndex;

    return (
        <div className="w-full overflow-x-auto pb-4 hide-scrollbar">
            <div className="flex items-center min-w-max px-2">
                {PHASES.map((phase: any, index: number) => {
                    const isCompleted = index < activeIndex;
                    const isCurrent = index === activeIndex;
                    const isPending = index > activeIndex;

                    return (
                        <div key={phase.id} className="flex items-center">
                            {/* Le point */}
                            <div className="relative flex flex-col items-center group">
                                <div
                                    className={cn(
                                        "w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-500 z-10 bg-background",
                                        isCompleted ? "border-emerald-500 text-emerald-500 bg-emerald-500/10" :
                                            isCurrent ? "border-brand-500 text-brand-500 bg-brand-500/10 shadow-[0_0_15px_rgba(var(--brand-500),0.5)]" :
                                                "border-muted text-muted-foreground"
                                    )}
                                >
                                    {isCompleted ? (
                                        <Check className="h-5 w-5" />
                                    ) : isCurrent ? (
                                        <Loader2 className="h-5 w-5 animate-spin" />
                                    ) : (
                                        <CircleDashed className="h-5 w-5 opacity-50" />
                                    )}
                                </div>

                                {/* Le label */}
                                <span className={cn(
                                    "absolute top-12 text-xs font-semibold whitespace-nowrap transition-colors duration-300",
                                    isCompleted ? "text-emerald-500" :
                                        isCurrent ? "text-brand-500" :
                                            "text-muted-foreground"
                                )}>
                                    {phase.label}
                                </span>
                            </div>

                            {/* La ligne de connexion */}
                            {index < PHASES.length - 1 && (
                                <div className="w-16 sm:w-24 h-1 mx-2 rounded-full overflow-hidden bg-muted relative">
                                    <div
                                        className={cn(
                                            "absolute top-0 left-0 h-full bg-emerald-500 transition-all duration-1000 ease-in-out",
                                            isCompleted ? "w-full" : "w-0"
                                        )}
                                    />
                                    {isCurrent && (
                                        <div className="absolute top-0 left-0 h-full w-full bg-gradient-to-r from-transparent via-brand-500/50 to-transparent flex shrink-0 animate-[shimmer_2s_infinite]" />
                                    )}
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

