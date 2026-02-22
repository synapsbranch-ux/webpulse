"use client";

import { motion } from "framer-motion";
import { Globe, Lock, Zap, ShieldAlert, Search } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const features = [
    {
        title: "DNS & Config",
        description: "Vérification des enregistrements A, MX, TXT et temps de résolution.",
        icon: Globe,
        color: "text-blue-500",
        bgColor: "bg-blue-500/10",
        borderColor: "border-blue-500/20"
    },
    {
        title: "Sécurité SSL",
        description: "Analyse de la chaîne de certificats, et protocoles supportés.",
        icon: Lock,
        color: "text-emerald-500",
        bgColor: "bg-emerald-500/10",
        borderColor: "border-emerald-500/20"
    },
    {
        title: "Performance",
        description: "Tests de montée en charge et temps de réponse moyen.",
        icon: Zap,
        color: "text-amber-500",
        bgColor: "bg-amber-500/10",
        borderColor: "border-amber-500/20"
    },
    {
        title: "Faille DAST",
        description: "Scan des failles communes (XSS, SQLi, Headers manquants).",
        icon: ShieldAlert,
        color: "text-red-500",
        bgColor: "bg-red-500/10",
        borderColor: "border-red-500/20"
    },
    {
        title: "SEO Audit",
        description: "Audit des balises meta, de la structure et accessibilité.",
        icon: Search,
        color: "text-purple-500",
        bgColor: "bg-purple-500/10",
        borderColor: "border-purple-500/20"
    },
];

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: { staggerChildren: 0.1 },
    },
};

const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export function Features() {
    return (
        <section className="py-24 bg-muted/10 relative border-t border-border/50">
            <div className="container px-4 mx-auto">
                <div className="mb-16 text-center">
                    <h2 className="mb-4 text-3xl font-bold tracking-tight md:text-4xl">
                        5 modules d'analyse complets
                    </h2>
                    <p className="mx-auto max-w-2xl text-muted-foreground text-lg">
                        Notre plateforme exécute une batterie de tests rigoureux pour vous donner
                        une vue d'ensemble de la santé de votre application web.
                    </p>
                </div>

                <motion.div
                    variants={containerVariants}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true, margin: "-100px" }}
                    className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5"
                >
                    {features.map((feature, index) => {
                        const Icon = feature.icon;
                        return (
                            <motion.div key={index} variants={itemVariants} className="h-full">
                                <Card className={`group h-full transition-all duration-300 hover:-translate-y-2 hover:shadow-xl hover:shadow-brand-500/5 ${feature.borderColor} bg-card/50 backdrop-blur-sm`}>
                                    <CardHeader>
                                        <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl ${feature.bgColor} transition-colors group-hover:bg-brand-500/10`}>
                                            <Icon className={`h-6 w-6 ${feature.color} group-hover:text-brand-500 transition-colors`} />
                                        </div>
                                        <CardTitle className="text-xl">{feature.title}</CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <CardDescription className="text-sm leading-relaxed">
                                            {feature.description}
                                        </CardDescription>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        );
                    })}
                </motion.div>
            </div>
        </section>
    );
}
