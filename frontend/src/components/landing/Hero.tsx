"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Globe, ArrowRight, Shield, Zap, Lock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function Hero() {
    const [url, setUrl] = useState("");
    const router = useRouter();

    const handleScan = (e: React.FormEvent) => {
        e.preventDefault();
        if (url) {
            router.push(`/new-scan?url=${encodeURIComponent(url)}`);
        }
    };

    return (
        <section className="relative overflow-hidden pt-32 pb-24 lg:pt-48 lg:pb-32 flex flex-col items-center justify-center min-h-[80vh]">
            <div className="absolute inset-0 z-0 bg-background overflow-hidden">
                <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-brand-900/40 via-background to-background"></div>
                <div className="absolute inset-0 bg-[radial-gradient(#ffffff15_1px,transparent_1px)] [background-size:20px_20px] opacity-30 [mask-image:linear-gradient(to_bottom,white,transparent)]"></div>
            </div>

            <div className="container relative z-10 mx-auto px-4 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="mx-auto max-w-4xl"
                >
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.2, duration: 0.5 }}
                        className="mb-8 inline-flex items-center gap-2 rounded-full border border-brand-500/20 bg-brand-500/10 px-4 py-1.5 text-sm font-medium text-brand-400"
                    >
                        <Shield className="h-4 w-4" />
                        <span>12,000+ sites analysés avec succès</span>
                    </motion.div>

                    <h1 className="mb-6 text-5xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
                        Analysez votre site web en <br className="hidden sm:block" />
                        <span className="bg-gradient-to-r from-brand-400 to-brand-600 bg-clip-text text-transparent">
                            profondeur
                        </span>
                    </h1>
                    <p className="mx-auto mb-10 max-w-2xl text-lg text-muted-foreground sm:text-xl">
                        Performance, Sécurité, SSL, DNS, SEO — Un scan complet en un clic.
                    </p>

                    <form onSubmit={handleScan} className="mx-auto mb-12 flex max-w-xl flex-col gap-4 sm:flex-row">
                        <div className="relative flex-1">
                            <Globe className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
                            <Input
                                type="url"
                                placeholder="https://example.com"
                                required
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                                className="h-14 pl-12 text-lg rounded-xl border-border bg-background/50 focus-visible:ring-brand-500 shadow-xl shadow-brand-500/5 transition-shadow"
                            />
                        </div>
                        <Button type="submit" size="lg" className="h-14 w-full sm:w-auto text-lg rounded-xl transition-all hover:scale-105 bg-brand-500 hover:bg-brand-600 shadow-lg shadow-brand-500/20">
                            Lancer le Scan
                            <ArrowRight className="ml-2 h-5 w-5" />
                        </Button>
                    </form>

                    <div className="flex flex-wrap items-center justify-center gap-6 text-sm text-muted-foreground">
                        <div className="flex items-center gap-2">
                            <Zap className="h-4 w-4 text-amber-500" />
                            <span>Diagnostic en temps réel</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <Lock className="h-4 w-4 text-emerald-500" />
                            <span>Rapport sécurisé & PDF</span>
                        </div>
                    </div>
                </motion.div>
            </div>
        </section>
    );
}
