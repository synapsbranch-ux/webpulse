import Link from "next/link";
import { Github, Twitter } from "lucide-react";

export function Footer() {
    return (
        <footer className="border-t border-border/50 bg-background pt-16 pb-8">
            <div className="container px-4 mx-auto">
                <div className="grid gap-8 md:grid-cols-4 mb-12">
                    <div className="md:col-span-1">
                        <Link href="/" className="flex items-center gap-2 mb-4">
                            <span className="bg-brand-500 rounded-md w-6 h-6 inline-flex items-center justify-center text-white text-xs font-bold">SB</span>
                            <span className="font-bold text-xl tracking-tight">synapsbranch</span>
                        </Link>
                        <p className="text-muted-foreground text-sm max-w-xs">
                            Plateforme SaaS d'analyse web automatisée. Optimisez la performance, la sécurité et l'architecture de votre présence en ligne en temps réel.
                        </p>
                    </div>

                    <div>
                        <h4 className="font-semibold mb-4">Produit</h4>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><Link href="#features" className="hover:text-brand-500 transition-colors">Fonctionnalités</Link></li>
                            <li><Link href="#pricing" className="hover:text-brand-500 transition-colors">Tarifs</Link></li>
                            <li><Link href="/dashboard" className="hover:text-brand-500 transition-colors">Dashboard</Link></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-semibold mb-4">Ressources</h4>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><Link href="#" className="hover:text-brand-500 transition-colors">Documentation</Link></li>
                            <li><Link href="#" className="hover:text-brand-500 transition-colors">Blog</Link></li>
                            <li><Link href="#" className="hover:text-brand-500 transition-colors">API Reference</Link></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-semibold mb-4">Légal</h4>
                        <ul className="space-y-2 text-sm text-muted-foreground">
                            <li><Link href="#" className="hover:text-brand-500 transition-colors">Conditions d'utilisation</Link></li>
                            <li><Link href="#" className="hover:text-brand-500 transition-colors">Politique de confidentialité</Link></li>
                        </ul>
                        <div className="flex gap-4 mt-6">
                            <Link href="#" className="text-muted-foreground hover:text-brand-500">
                                <Github className="h-5 w-5" />
                                <span className="sr-only">GitHub</span>
                            </Link>
                            <Link href="#" className="text-muted-foreground hover:text-brand-500">
                                <Twitter className="h-5 w-5" />
                                <span className="sr-only">Twitter</span>
                            </Link>
                        </div>
                    </div>
                </div>

                <div className="pt-8 border-t border-border/50 text-center text-sm text-muted-foreground">
                    <p>© {new Date().getFullYear()} synapsbranch. Tous droits réservés.</p>
                </div>
            </div>
        </footer>
    );
}
