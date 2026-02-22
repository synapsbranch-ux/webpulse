"use client";

import { Report } from "@/types/report";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { OverviewPanel } from "@/components/report/OverviewPanel";
import { ShieldAlert, Zap, Lock, Globe, Search, LayoutDashboard } from "lucide-react";

interface ReportViewerProps {
    report: Report;
}

export function ReportViewer({ report }: ReportViewerProps) {
    return (
        <Tabs defaultValue="overview" className="w-full">
            <div className="overflow-x-auto pb-4 hide-scrollbar">
                <TabsList className="bg-muted/50 w-max inline-flex">
                    <TabsTrigger value="overview" className="gap-2 px-4">
                        <LayoutDashboard className="h-4 w-4" /> Vue Globale
                    </TabsTrigger>
                    <TabsTrigger value="perf" className="gap-2 px-4">
                        <Zap className="h-4 w-4 text-amber-500" /> Performance
                    </TabsTrigger>
                    <TabsTrigger value="dast" className="gap-2 px-4">
                        <ShieldAlert className="h-4 w-4 text-red-500" /> Sécurité
                    </TabsTrigger>
                    <TabsTrigger value="ssl" className="gap-2 px-4">
                        <Lock className="h-4 w-4 text-emerald-500" /> SSL
                    </TabsTrigger>
                    <TabsTrigger value="dns" className="gap-2 px-4">
                        <Globe className="h-4 w-4 text-blue-500" /> DNS / Réseau
                    </TabsTrigger>
                    <TabsTrigger value="seo" className="gap-2 px-4">
                        <Search className="h-4 w-4 text-purple-500" /> SEO
                    </TabsTrigger>
                </TabsList>
            </div>

            <div className="mt-6">
                <TabsContent value="overview" className="m-0 focus-visible:outline-none focus-visible:ring-0">
                    <OverviewPanel report={report} />
                </TabsContent>

                {/* Placeholders for other tabs */}
                <TabsContent value="perf" className="m-0">
                    <div className="p-12 text-center border rounded-xl border-dashed">Module Performance en développement</div>
                </TabsContent>
                <TabsContent value="dast" className="m-0">
                    <div className="p-12 text-center border rounded-xl border-dashed">Module Sécurité en développement</div>
                </TabsContent>
                <TabsContent value="ssl" className="m-0">
                    <div className="p-12 text-center border rounded-xl border-dashed">Module SSL en développement</div>
                </TabsContent>
                <TabsContent value="dns" className="m-0">
                    <div className="p-12 text-center border rounded-xl border-dashed">Module DNS en développement</div>
                </TabsContent>
                <TabsContent value="seo" className="m-0">
                    <div className="p-12 text-center border rounded-xl border-dashed">Module SEO en développement</div>
                </TabsContent>
            </div>
        </Tabs>
    );
}
