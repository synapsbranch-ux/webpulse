"use client";

import { Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { useRouter } from "next/navigation";

const plans = [
    {
        name: "Free",
        price: "0€",
        description: "Pour les petits projets personnels",
        features: [
            "10 scans par mois",
            "Tests DNS & SSL basiques",
            "Rapport PDF standard",
            "Support communautaire"
        ],
        cta: "Commencer",
        popular: false,
    },
    {
        name: "Pro",
        price: "29€",
        period: "/mois",
        description: "Pour les professionnels et agences",
        features: [
            "Scans illimités",
            "Tests de performance avancés",
            "Analyse de sécurité DAST complète",
            "Rapports IA personnalisés avec recommandations",
            "Support prioritaire"
        ],
        cta: "Essai gratuit de 14 jours",
        popular: true,
    },
    {
        name: "Enterprise",
        price: "Sur mesure",
        description: "Pour les applications critiques",
        features: [
            "Instances dédiées",
            "Tests de charge > 10,000 utilisateurs",
            "API intégration CI/CD",
            "SLA garanti 99.9%",
            "Account manager dédié"
        ],
        cta: "Contacter les ventes",
        popular: false,
    }
];

export function Pricing() {
    const router = useRouter();

    return (
        <section className="py-24 bg-muted/10 relative">
            <div className="container px-4 mx-auto">
                <div className="mb-16 text-center">
                    <h2 className="mb-4 text-3xl font-bold tracking-tight md:text-4xl">
                        Des tarifs simples et transparents
                    </h2>
                    <p className="mx-auto max-w-2xl text-muted-foreground text-lg">
                        Choisissez le plan qui correspond à vos besoins d'analyse web.
                    </p>
                </div>

                <div className="grid gap-8 lg:grid-cols-3 max-w-6xl mx-auto">
                    {plans.map((plan, index) => (
                        <Card key={index} className={`flex flex-col relative ${plan.popular ? 'border-brand-500 shadow-2xl shadow-brand-500/10' : 'border-border/50'}`}>
                            {plan.popular && (
                                <div className="absolute top-0 inset-x-0 -translate-y-1/2 flex justify-center">
                                    <span className="bg-brand-500 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                                        Le plus populaire
                                    </span>
                                </div>
                            )}
                            <CardHeader className="text-center pb-2">
                                <CardTitle className="text-2xl font-bold">{plan.name}</CardTitle>
                                <CardDescription className="h-10">{plan.description}</CardDescription>
                                <div className="mt-4 flex items-baseline justify-center text-5xl font-extrabold">
                                    {plan.price}
                                    {plan.period && <span className="text-xl text-muted-foreground font-medium ml-1">{plan.period}</span>}
                                </div>
                            </CardHeader>
                            <CardContent className="flex-1 mt-6">
                                <ul className="space-y-4">
                                    {plan.features.map((feature, i) => (
                                        <li key={i} className="flex items-start">
                                            <Check className="h-5 w-5 text-brand-500 shrink-0 mr-3" />
                                            <span className="text-muted-foreground">{feature}</span>
                                        </li>
                                    ))}
                                </ul>
                            </CardContent>
                            <CardFooter>
                                <Button
                                    onClick={() => router.push('/register')}
                                    variant={plan.popular ? "default" : "outline"}
                                    className={`w-full ${plan.popular ? 'bg-brand-500 hover:bg-brand-600' : ''}`}
                                >
                                    {plan.cta}
                                </Button>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            </div>
        </section>
    );
}
