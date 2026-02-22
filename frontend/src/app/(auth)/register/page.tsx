import Link from "next/link";
import Image from "next/image";
import { ArrowLeft } from "lucide-react";
import { RegisterForm } from "@/components/auth/RegisterForm";
import { SocialButtons } from "@/components/auth/SocialButtons";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function RegisterPage() {
    return (
        <Card className="border-border/50 shadow-2xl shadow-brand-500/10">
            <CardHeader className="space-y-4 text-center">
                <div className="flex justify-start">
                    <Button variant="ghost" size="sm" asChild className="text-muted-foreground hover:text-foreground -ml-2">
                        <Link href="/">
                            <ArrowLeft className="mr-2 h-4 w-4" />
                            Retour à l'accueil
                        </Link>
                    </Button>
                </div>
                <div className="mx-auto flex h-20 w-20 items-center justify-center relative">
                    <Image
                        src="/assets/synapsbranch.png"
                        alt="Logo Synapsbranch"
                        fill
                        className="object-contain"
                    />
                </div>
                <div>
                    <CardTitle className="text-2xl">Créer un compte</CardTitle>
                    <CardDescription>
                        Rejoignez synapsbranch pour analyser vos sites
                    </CardDescription>
                </div>
            </CardHeader>
            <CardContent className="space-y-4">
                <SocialButtons />

                <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                        <span className="w-full border-t border-border/50" />
                    </div>
                    <div className="relative flex justify-center text-xs uppercase">
                        <span className="bg-card px-2 text-muted-foreground">ou s'inscrire avec l'email</span>
                    </div>
                </div>

                <RegisterForm />
            </CardContent>
            <CardFooter className="flex justify-center border-t border-border/50 p-4">
                <p className="text-sm text-muted-foreground">
                    Déjà un compte ?{" "}
                    <Link href="/login" className="text-brand-500 hover:underline font-medium">
                        Se connecter
                    </Link>
                </p>
            </CardFooter>
        </Card>
    );
}
