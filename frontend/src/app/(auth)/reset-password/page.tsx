import { KeyRound } from "lucide-react";
import { ResetPasswordForm } from "@/components/auth/ResetPasswordForm";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function ResetPasswordPage() {
    return (
        <Card className="border-border/50 shadow-2xl shadow-brand-500/10">
            <CardHeader className="space-y-4 text-center">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-brand-500/10 text-brand-500">
                    <KeyRound className="h-8 w-8" />
                </div>
                <CardTitle className="text-2xl">Nouveau mot de passe</CardTitle>
                <CardDescription>
                    Veuillez entrer votre nouveau mot de passe ci-dessous.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <ResetPasswordForm />
            </CardContent>
        </Card>
    );
}
