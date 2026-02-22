import Link from "next/link";
import { LoginForm } from "@/components/auth/LoginForm";
import { SocialButtons } from "@/components/auth/SocialButtons";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function LoginPage() {
    return (
        <Card className="border-border/50 shadow-2xl shadow-brand-500/10">
            <CardHeader className="space-y-2 text-center">
                <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-brand-500 text-white font-bold text-xl">
                    SB
                </div>
                <CardTitle className="text-2xl">Bon retour</CardTitle>
                <CardDescription>
                    Connectez-vous à votre compte synapsbranch
                </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
                <SocialButtons />

                <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                        <span className="w-full border-t border-border/50" />
                    </div>
                    <div className="relative flex justify-center text-xs uppercase">
                        <span className="bg-card px-2 text-muted-foreground">ou continuer avec l'email</span>
                    </div>
                </div>

                <LoginForm />

                <div className="text-center text-sm mt-4">
                    <Link href="/forgot-password" className="text-brand-500 hover:underline">
                        Mot de passe oublié ?
                    </Link>
                </div>
            </CardContent>
            <CardFooter className="flex justify-center border-t border-border/50 p-4">
                <p className="text-sm text-muted-foreground">
                    Pas de compte ?{" "}
                    <Link href="/register" className="text-brand-500 hover:underline font-medium">
                        S'inscrire
                    </Link>
                </p>
            </CardFooter>
        </Card>
    );
}
