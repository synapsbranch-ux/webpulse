"use client";

import { motion } from "framer-motion";
import { Link, Activity, FileText, ArrowRight } from "lucide-react";

const steps = [
    {
        title: "Entrez votre URL",
        description: "Indiquez l'adresse de votre site web à analyser. Aucun code à installer.",
        icon: Link,
    },
    {
        title: "Observez le scan en direct",
        description: "Suivez l'avancement des 5 modules d'analyse en temps réel via notre interface WebSocket.",
        icon: Activity,
    },
    {
        title: "Recevez votre rapport IA",
        description: "Obtenez un rapport détaillé avec des recommandations générées par notre IA.",
        icon: FileText,
    },
];

export function HowItWorks() {
    return (
        <section className="py-24 relative overflow-hidden">
            <div className="container px-4 mx-auto">
                <div className="mb-16 text-center">
                    <h2 className="mb-4 text-3xl font-bold tracking-tight md:text-4xl">
                        Comment ça marche ?
                    </h2>
                    <p className="mx-auto max-w-2xl text-muted-foreground text-lg">
                        Un processus simple, transparent et extrêmement rapide.
                    </p>
                </div>

                <div className="relative max-w-5xl mx-auto">
                    {/* Ligne connectrice (hidden sur mobile) */}
                    <div className="absolute top-1/2 left-0 w-full h-0.5 bg-border/50 -translate-y-1/2 hidden md:block" />

                    <div className="grid gap-12 md:gap-6 md:grid-cols-3">
                        {steps.map((step, index) => {
                            const Icon = step.icon;
                            return (
                                <motion.div
                                    key={index}
                                    initial={{ opacity: 0, y: 20 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    viewport={{ once: true, margin: "-100px" }}
                                    transition={{ duration: 0.5, delay: index * 0.2 }}
                                    className="relative flex flex-col items-center text-center space-y-4"
                                >
                                    <div className="relative z-10 flex h-20 w-20 items-center justify-center rounded-full bg-background border-2 border-brand-500 shadow-lg shadow-brand-500/20">
                                        <Icon className="h-8 w-8 text-brand-500" />
                                        <div className="absolute -top-2 -right-2 flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground font-bold text-sm">
                                            {index + 1}
                                        </div>
                                    </div>
                                    <h3 className="text-xl font-semibold mt-4">{step.title}</h3>
                                    <p className="text-muted-foreground leading-relaxed">
                                        {step.description}
                                    </p>
                                </motion.div>
                            );
                        })}
                    </div>
                </div>
            </div>
        </section>
    );
}
