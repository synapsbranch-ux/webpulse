import { useEffect, useState } from 'react';
import { useScanStore } from '@/stores/scanStore';
import { connectToScan } from '@/lib/socket';
import { LiveMetrics } from '@/types/scan';

export function useLiveResults(scanId: string | undefined) {
    const {
        logs,
        liveMetrics,
        currentPhase,
        phaseResults,
        overallScore,
        isComplete,
        isReportReady,
        addLog,
        updateMetrics,
        setPhase,
        completeModule,
        completeScan,
        setReportReady
    } = useScanStore();

    const [isConnected, setIsConnected] = useState(false);
    const [metricsStream, setMetricsStream] = useState<LiveMetrics[]>([]);
    const [error, setError] = useState<string | null>(null);

    // Keep history of metrics for charts
    useEffect(() => {
        if (liveMetrics) {
            setMetricsStream(prev => {
                const newStream = [...prev, liveMetrics];
                // Keep only last 50 points
                if (newStream.length > 50) return newStream.slice(newStream.length - 50);
                return newStream;
            });
        }
    }, [liveMetrics]);

    useEffect(() => {
        if (!scanId || isComplete) return;

        setIsConnected(true);
        setError(null);

        const cleanup = connectToScan(
            scanId,
            (msg) => {
                switch (msg.type) {
                    case 'phase_change':
                        if (msg.phase) setPhase(msg.phase);
                        break;
                    case 'log':
                        if (msg.entry) addLog(msg.entry);
                        break;
                    case 'progress':
                        if (msg.metrics) updateMetrics(msg.metrics);
                        break;
                    case 'module_complete':
                        if (msg.phase && typeof msg.score === 'number' && msg.grade) {
                            completeModule(msg.phase, msg.score, msg.grade);
                        }
                        break;
                    case 'scan_complete':
                        if (typeof msg.score === 'number') completeScan(msg.score);
                        break;
                    case 'report_ready':
                        setReportReady();
                        break;
                    case 'error':
                        if (msg.error) setError(msg.error);
                        break;
                    default:
                        console.warn('Unknown WS Message type', msg);
                }
            },
            () => {
                setIsConnected(false);
            }
        );

        return () => {
            cleanup();
            setIsConnected(false);
        };
    }, [
        scanId,
        isComplete,
        setPhase,
        addLog,
        updateMetrics,
        completeModule,
        completeScan,
        setReportReady
    ]);

    const disconnect = () => {
        setIsConnected(false);
    };

    return {
        isConnected,
        error,
        disconnect,
        logs,
        liveMetrics,
        metricsStream,
        currentPhase,
        phaseResults,
        overallScore,
        isComplete,
        isReportReady
    };
}

