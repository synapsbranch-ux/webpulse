import Link from "next/link";
import { KeyRound } from "lucide-react";
import { ForgotPasswordForm } from "@/components/auth/ForgotPasswordForm";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function ForgotPasswordPage() {
    return (
        <Card className="border-border/50 shadow-2xl shadow-brand-500/10">
            <CardHeader className="space-y-4 text-center">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-brand-500/10 text-brand-500">
                    <KeyRound className="h-8 w-8" />
                </div>
                <CardTitle className="text-2xl">Mot de passe oublié</CardTitle>
                <CardDescription>
                    Entrez votre email et nous vous enverrons un lien pour réinitialiser votre mot de passe.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <ForgotPasswordForm />
            </CardContent>
            <CardFooter className="flex justify-center border-t border-border/50 p-4">
                <Link href="/login" className="text-brand-500 text-sm hover:underline font-medium">
                    Retour à la connexion
                </Link>
            </CardFooter>
        </Card>
    );
}
