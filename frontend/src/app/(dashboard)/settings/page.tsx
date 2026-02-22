"use client";

import { useAuth } from "@/hooks/useAuth";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Settings, Save, User } from "lucide-react";

export default function SettingsPage() {
    const { user } = useAuth();

    return (
        <div className="space-y-8 animate-in fade-in duration-500 slide-in-from-bottom-4 pb-12 max-w-4xl mx-auto">
            <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-500/10 text-brand-500">
                    <Settings className="h-6 w-6" />
                </div>
                <div>
                    <h2 className="text-2xl font-bold tracking-tight">Paramètres du Compte</h2>
                    <p className="text-muted-foreground">Gérez votre profil et vos préférences de compte.</p>
                </div>
            </div>

            <div className="grid gap-8">
                <Card className="border-border/50 shadow-lg bg-card/60 backdrop-blur-sm">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 font-bold">
                            <User className="h-5 w-5 text-brand-500" />
                            Profil Utilisateur
                        </CardTitle>
                        <CardDescription>
                            Mettez à jour vos informations personnelles.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="name">Nom / Entreprise</Label>
                                <Input
                                    id="name"
                                    defaultValue={user?.name || ""}
                                    placeholder="Votre nom"
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="email">Adresse mail</Label>
                                <Input
                                    id="email"
                                    type="email"
                                    defaultValue={user?.email || ""}
                                    placeholder="nom@exemple.com"
                                    disabled
                                />
                                <p className="text-xs text-muted-foreground">Votre adresse email ne peut pas être modifiée ici.</p>
                            </div>
                        </div>
                    </CardContent>
                    <CardFooter className="flex justify-end border-t border-border/50 bg-muted/20 px-6 py-4">
                        <Button className="bg-brand-500 hover:bg-brand-600 shadow-lg shadow-brand-500/20">
                            <Save className="mr-2 h-4 w-4" /> Enregistrer les modifications
                        </Button>
                    </CardFooter>
                </Card>

                {/* Placeholder pour Password / API Keys */}
                <Card className="border-border/50 shadow-lg bg-card/60 backdrop-blur-sm">
                    <CardHeader>
                        <CardTitle className="font-bold">Mot de passe</CardTitle>
                        <CardDescription>Changez votre mot de passe pour sécuriser votre compte.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="current_password">Mot de passe actuel</Label>
                            <Input id="current_password" type="password" />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="new_password">Nouveau mot de passe</Label>
                            <Input id="new_password" type="password" />
                        </div>
                    </CardContent>
                    <CardFooter className="flex justify-end border-t border-border/50 bg-muted/20 px-6 py-4">
                        <Button variant="secondary">
                            Mettre à jour
                        </Button>
                    </CardFooter>
                </Card>
            </div>
        </div>
    );
}
