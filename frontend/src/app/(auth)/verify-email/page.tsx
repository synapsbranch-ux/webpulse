"use client";

import Link from "next/link";
import { MailCheck, CheckCircle2, XCircle, Loader2 } from "lucide-react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function VerifyEmailPage() {
    const searchParams = useSearchParams();
    const token = searchParams.get("token");

    const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
    const [message, setMessage] = useState("");

    useEffect(() => {
        if (!token) {
            setStatus("idle");
            return;
        }

        const verifyToken = async () => {
            setStatus("loading");
            try {
                const response = await api.get(`/auth/verify-email?token=${token}`);
                setStatus("success");
                setMessage(response.data.message || "Email vérifié avec succès.");
            } catch (error: any) {
                setStatus("error");
                setMessage(error.response?.data?.detail || "Le lien de vérification est invalide ou a expiré.");
            }
        };

        verifyToken();
    }, [token]);

    return (
        <Card className="border-border/50 shadow-2xl shadow-brand-500/10 text-center">
            <CardHeader className="space-y-4">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-brand-500/10 text-brand-500">
                    {status === "loading" ? (
                        <Loader2 className="h-8 w-8 animate-spin" />
                    ) : status === "success" ? (
                        <CheckCircle2 className="h-8 w-8 text-success" />
                    ) : status === "error" ? (
                        <XCircle className="h-8 w-8 text-destructive" />
                    ) : (
                        <MailCheck className="h-8 w-8" />
                    )}
                </div>
                <CardTitle className="text-2xl">
                    {status === "success" ? "Email Vérifié" :
                        status === "error" ? "Erreur de Vérification" :
                            "Vérifiez votre email"}
                </CardTitle>
                <CardDescription className="text-base text-balance">
                    {status === "success" ? message :
                        status === "error" ? message :
                            "Nous vous avons envoyé un lien de confirmation. Veuillez cliquer sur ce lien pour activer votre compte."}
                </CardDescription>
            </CardHeader>
            <CardContent>
                {(!token || status === "idle") && (
                    <div className="text-sm text-muted-foreground mb-4">
                        Vous n'avez pas reçu l'email ? Regardez dans vos spams.
                    </div>
                )}
            </CardContent>
            <CardFooter className="justify-center border-t border-border/50 p-4">
                <Link href="/login" className="text-brand-500 text-sm hover:underline font-medium">
                    {status === "success" ? "Aller à la page de connexion" : "Retour à la connexion"}
                </Link>
            </CardFooter>
        </Card>
    );
}

