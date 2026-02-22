"use client";

import * as z from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Loader2 } from "lucide-react";
import { api } from "@/lib/api";

const resetPasswordSchema = z.object({
    password: z.string().min(8, { message: "Au moins 8 caractères" }),
    confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
    message: "Les mots de passe ne correspondent pas",
    path: ["confirmPassword"],
});

type ResetPasswordValues = z.infer<typeof resetPasswordSchema>;

export function ResetPasswordForm() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const token = searchParams.get("token");
    const [isLoading, setIsLoading] = useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<ResetPasswordValues>({
        resolver: zodResolver(resetPasswordSchema),
    });

    const onSubmit = async (data: ResetPasswordValues) => {
        if (!token) {
            toast.error("Token manquant ou invalide.");
            return;
        }
        setIsLoading(true);
        try {
            await api.post("/auth/reset-password", { token, new_password: data.password });
            toast.success("Mot de passe réinitialisé avec succès.");
            router.push("/login");
        } catch (error: any) {
            toast.error(error?.response?.data?.detail || "Erreur de réinitialisation");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="space-y-2">
                <Label htmlFor="password">Nouveau mot de passe</Label>
                <Input
                    id="password"
                    type="password"
                    disabled={isLoading}
                    {...register("password")}
                />
                {errors.password && <p className="text-sm text-destructive">{errors.password.message}</p>}
            </div>
            <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirmez le nouveau mot de passe</Label>
                <Input
                    id="confirmPassword"
                    type="password"
                    disabled={isLoading}
                    {...register("confirmPassword")}
                />
                {errors.confirmPassword && <p className="text-sm text-destructive">{errors.confirmPassword.message}</p>}
            </div>
            <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Réinitialiser
            </Button>
        </form>
    );
}
