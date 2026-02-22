import { create } from 'zustand';
import { Scan, LogEntry, LiveMetrics } from '@/types/scan';

interface ScanState {
    currentScan: Scan | null;
    logs: LogEntry[];
    liveMetrics: LiveMetrics | null;
    currentPhase: string;
    phaseResults: Record<string, { score: number; grade: string }>;
    overallScore: number | null;
    isComplete: boolean;
    isReportReady: boolean;
    addLog: (entry: LogEntry) => void;
    updateMetrics: (metrics: LiveMetrics) => void;
    setPhase: (phase: string) => void;
    completeModule: (phase: string, score: number, grade: string) => void;
    completeScan: (score: number) => void;
    setReportReady: () => void;
    reset: () => void;
    setCurrentScan: (scan: Scan) => void;
}

export const useScanStore = create<ScanState>((set) => ({
    currentScan: null,
    logs: [],
    liveMetrics: null,
    currentPhase: 'pending',
    phaseResults: {},
    overallScore: null,
    isComplete: false,
    isReportReady: false,

    addLog: (entry) => set((state) => ({ logs: [...state.logs, entry] })),

    updateMetrics: (metrics) => set({ liveMetrics: metrics }),

    setPhase: (phase) => set({ currentPhase: phase }),

    completeModule: (phase, score, grade) => set((state) => ({
        phaseResults: {
            ...state.phaseResults,
            [phase]: { score, grade }
        }
    })),

    completeScan: (score) => set({ isComplete: true, overallScore: score }),

    setReportReady: () => set({ isReportReady: true }),

    setCurrentScan: (scan) => set({ currentScan: scan }),

    reset: () => set({
        currentScan: null,
        logs: [],
        liveMetrics: null,
        currentPhase: 'pending',
        phaseResults: {},
        overallScore: null,
        isComplete: false,
        isReportReady: false
    })
}));
