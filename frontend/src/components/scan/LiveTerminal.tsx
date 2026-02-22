"use client";

import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { LogEntry } from "@/types/scan";
import { ScrollArea } from "@/components/ui/scroll-area";
import { formatDate } from "@/lib/utils";

interface LiveTerminalProps {
    logs: LogEntry[];
    isScanning: boolean;
}

export function LiveTerminal({ logs, isScanning }: LiveTerminalProps) {
    const endRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [logs]);

    const getLogColor = (level: string) => {
        switch (level) {
            case 'error': return 'text-red-500';
            case 'warning': return 'text-amber-500';
            case 'success': return 'text-emerald-500';
            default: return 'text-muted-foreground';
        }
    };

    return (
        <div className="rounded-xl border border-border/50 bg-[#0A0A0A] overflow-hidden shadow-2xl shadow-brand-500/5 font-mono text-sm">
            <div className="flex items-center gap-2 px-4 py-3 border-b border-white/10 bg-[#111]">
                <div className="flex gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-red-500/80" />
                    <div className="w-3 h-3 rounded-full bg-amber-500/80" />
                    <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
                </div>
                <div className="ml-4 text-xs font-semibold text-muted-foreground tracking-wide flex items-center">
                    Terminal d'exécution
                    {isScanning && (
                        <span className="ml-3 flex h-2 w-2 relative">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-500"></span>
                        </span>
                    )}
                </div>
            </div>

            <ScrollArea className="h-[300px] w-full p-4">
                <div className="space-y-1">
                    <AnimatePresence initial={false}>
                        {logs.map((log, i) => (
                            <motion.div
                                key={log.id || i}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.2 }}
                                className="flex gap-4 font-mono leading-relaxed"
                            >
                                <div className="text-muted-foreground/50 shrink-0 w-[140px]">
                                    {formatDate(log.timestamp)}
                                </div>
                                <div>
                                    <span className={`mr-2 font-bold ${getLogColor(log.level)}`}>
                                        [{log.phase.toUpperCase()}]
                                    </span>
                                    <span className="text-gray-300">
                                        {log.message}
                                    </span>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                    {isScanning && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: [0, 1, 0] }}
                            transition={{ repeat: Infinity, duration: 1 }}
                            className="inline-block w-2.5 h-4 bg-brand-500 mt-1 ml-[156px]"
                        />
                    )}
                    <div ref={endRef} />
                </div>
            </ScrollArea>
        </div>
    );
}
