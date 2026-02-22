"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import * as z from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";
import { useScan } from "@/hooks/useScan";

import { Globe, ArrowRight, Shield, Zap, Lock, Search, ShieldAlert, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const scanSchema = z.object({
    url: z.string().url({ message: "Veuillez entrer une URL valide (ex: https://example.com)" }),
});

type ScanValues = z.infer<typeof scanSchema>;

const TESTS = [
    { id: 'dns', label: 'DNS & Réseau', icon: Globe, color: 'text-blue-500', bg: 'bg-blue-500/10' },
    { id: 'ssl', label: 'Sécurité SSL', icon: Lock, color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
    { id: 'perf', label: 'Performance', icon: Zap, color: 'text-amber-500', bg: 'bg-amber-500/10' },
    { id: 'dast', label: 'Faille DAST', icon: ShieldAlert, color: 'text-red-500', bg: 'bg-red-500/10' },
    { id: 'seo', label: 'Audit SEO', icon: Search, color: 'text-purple-500', bg: 'bg-purple-500/10' },
];

export function ScanForm() {
    const { startScan, isLoading } = useScan();
    const router = useRouter();
    const searchParams = useSearchParams();
    const initialUrl = searchParams.get("url");

    const { register, handleSubmit, formState: { errors }, setValue } = useForm<ScanValues>({
        resolver: zodResolver(scanSchema),
        defaultValues: {
            url: initialUrl || "",
        }
    });

    useEffect(() => {
        if (initialUrl) {
            setValue("url", initialUrl);
        }
    }, [initialUrl, setValue]);

    const onSubmit = async (data: ScanValues) => {
        try {
            const scan = await startScan(data.url);
            toast.success("Analyse démarrée");
            router.push(`/scan/${scan.id}`);
        } catch (e) {
            toast.error("Impossible de lancer le scan");
        }
    };

    return (
        <div className="max-w-3xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="text-center space-y-4">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-brand-500/10 text-brand-500">
                    <Globe className="h-8 w-8" />
                </div>
                <h1 className="text-3xl font-bold tracking-tight">Nouvelle Analyse</h1>
                <p className="text-muted-foreground text-lg">
                    Entrez l'URL de votre site pour démarrer une batterie de tests complète en temps réel.
                </p>
            </div>

            <Card className="border-border/50 shadow-2xl shadow-brand-500/5 bg-card/50 backdrop-blur-sm">
                <CardContent className="pt-6">
                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                        <div className="space-y-2">
                            <div className="relative">
                                <Globe className="absolute left-4 top-1/2 h-6 w-6 -translate-y-1/2 text-muted-foreground" />
                                <Input
                                    type="url"
                                    placeholder="https://example.com"
                                    className="h-16 pl-14 text-lg rounded-xl border-border focus-visible:ring-brand-500"
                                    disabled={isLoading}
                                    {...register("url")}
                                />
                            </div>
                            {errors.url && (
                                <p className="text-sm text-destructive font-medium pl-2">{errors.url.message}</p>
                            )}
                        </div>

                        <Button
                            type="submit"
                            size="lg"
                            className="w-full h-14 text-lg rounded-xl bg-brand-500 hover:bg-brand-600 shadow-lg shadow-brand-500/20"
                            disabled={isLoading}
                        >
                            {isLoading ? (
                                <>
                                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                                    Initialisation des tests...
                                </>
                            ) : (
                                <>
                                    Lancer le Scan complet
                                    <ArrowRight className="ml-2 h-5 w-5" />
                                </>
                            )}
                        </Button>
                    </form>
                </CardContent>
            </Card>

            <div className="pt-8">
                <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider text-center mb-6">
                    Tests qui seront effectués
                </h3>
                <div className="flex flex-wrap justify-center gap-3">
                    {TESTS.map((test) => {
                        const Icon = test.icon;
                        return (
                            <Badge
                                key={test.id}
                                variant="outline"
                                className={`flex items-center gap-2 py-2 px-4 shadow-sm ${test.bg} ${test.color} border-current/20 font-medium`}
                            >
                                <Icon className="h-4 w-4" />
                                {test.label}
                            </Badge>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
