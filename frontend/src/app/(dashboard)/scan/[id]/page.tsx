"use client";

import { useEffect, useState, use } from "react";
import { useLiveResults } from "@/hooks/useLiveResults";
import { useScan } from "@/hooks/useScan";
import { useRouter } from "next/navigation";

import { LiveTerminal } from "@/components/scan/LiveTerminal";
import { LiveMetrics } from "@/components/scan/LiveMetrics";
import { ScanProgress } from "@/components/scan/ScanProgress";
import { PhaseIndicator } from "@/components/scan/PhaseIndicator";
import { ScanComplete } from "@/components/scan/ScanComplete";
import { LiveLineChart } from "@/components/charts/LiveLineChart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { AlertCircle } from "lucide-react";

export default function LiveScanPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = use(params);
    const { getScan } = useScan();
    const router = useRouter();

    const {
        isConnected,
        error: wsError,
        disconnect,
        logs,
        liveMetrics,
        metricsStream,
        currentPhase,
        isComplete,
        isReportReady
    } = useLiveResults(id);

    const [scanData, setScanData] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        let active = true;

        getScan(id)
            .then(data => {
                if (active) {
                    setScanData(data);
                    setIsLoading(false);
                    // If the API says it's already done but WS store doesn't know
                    if (data.status === 'completed' && !isComplete) {
                        // The store handle the overall score, we should perhaps set it
                    }
                }
            })
            .catch(err => {
                if (active) setIsLoading(false);
            });

        return () => {
            active = false;
        };
    }, [id, getScan]);

    useEffect(() => {
        if (isReportReady) {
            router.push(`/scan/${id}/report`);
        }
    }, [isReportReady, id, router]);

    const isScanning = !isComplete && scanData?.status !== 'completed' && scanData?.status !== 'failed';

    if (isLoading) {
        return (
            <div className="space-y-6 animate-in fade-in">
                <Skeleton className="h-12 w-1/3" />
                <Skeleton className="h-24 w-full" />
                <Skeleton className="h-40 w-full" />
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <Skeleton className="h-[300px]" />
                    <Skeleton className="h-[300px]" />
                </div>
            </div>
        );
    }

    if (!scanData && !isLoading) {
        return (
            <div className="flex flex-col items-center justify-center p-12 text-center rounded-2xl border border-red-500/20 bg-red-500/5">
                <AlertCircle className="h-12 w-12 text-red-500 mb-4" />
                <h2 className="text-xl font-bold mb-2">Scan Introuvable</h2>
                <p className="text-muted-foreground">Impossible de trouver les informations pour ce scan.</p>
            </div>
        );
    }

    if (isComplete || scanData?.status === 'completed') {
        return <ScanComplete scan={scanData} />;
    }

    return (
        <div className="space-y-8 pb-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="mb-8">
                <h1 className="text-2xl font-bold tracking-tight mb-2">Analyse en cours</h1>
                <p className="text-muted-foreground flex items-center gap-2">
                    Cible: <span className="font-semibold text-foreground">{scanData?.url}</span>
                    {!isConnected && isScanning && (
                        <span className="text-amber-500 text-sm ml-2 font-medium">(Reconnexion au serveur...)</span>
                    )}
                </p>
                {wsError && (
                    <p className="text-red-500 text-sm mt-2 flex items-center font-medium">
                        <AlertCircle className="h-4 w-4 mr-2" />
                        {wsError}
                    </p>
                )}
            </div>

            <div className="bg-card/30 rounded-2xl p-6 border border-border/50 backdrop-blur-sm shadow-xl shadow-brand-500/5">
                <PhaseIndicator currentPhase={currentPhase || scanData?.current_phase || 'dns'} />
                <div className="mt-8">
                    <ScanProgress currentPhase={currentPhase || scanData?.current_phase || 'dns'} />
                </div>
            </div>

            <LiveMetrics metrics={liveMetrics} isLoading={!liveMetrics && isScanning} />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                    <Card className="h-full border-border/50 bg-card/60 backdrop-blur-md shadow-lg">
                        <CardHeader>
                            <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
                                Console d'Exécution
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <LiveTerminal logs={logs} isScanning={isScanning} />
                        </CardContent>
                    </Card>
                </div>

                <div className="lg:col-span-1 flex flex-col gap-6">
                    <Card className="flex-1 border-border/50 bg-card/60 backdrop-blur-md shadow-lg">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
                                Temps de Réponse en direct
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <LiveLineChart
                                dataStream={metricsStream}
                                dataKey="responseTime"
                                color="#f59e0b"
                                name="ms"
                            />
                        </CardContent>
                    </Card>
                    <Card className="flex-1 border-border/50 bg-card/60 backdrop-blur-md shadow-lg">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
                                Débit en direct
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <LiveLineChart
                                dataStream={metricsStream}
                                dataKey="throughput"
                                color="#10b981"
                                name="req/s"
                            />
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}

