"use client";

import { useAuth } from "@/hooks/useAuth";
import { ThemeToggle } from "./ThemeToggle";
import { MobileNav } from "./MobileNav";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { LogOut, User as UserIcon, Settings } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export function Header() {
    const { user, logout } = useAuth();
    const router = useRouter();

    const handleLogout = () => {
        logout();
        router.push("/login");
    };

    const getInitials = (name: string) => {
        if (!name) return "U";
        return name.slice(0, 2).toUpperCase();
    };

    return (
        <header className="sticky top-0 z-40 w-full border-b border-border/50 bg-background/80 backdrop-blur-md">
            <div className="flex h-16 items-center justify-between px-4 sm:px-6">
                <div className="flex items-center gap-4">
                    <MobileNav />
                    <div className="hidden sm:block">
                        <h1 className="text-xl font-bold tracking-tight text-foreground flex items-center gap-2">
                            <span className="bg-brand-500 rounded-md w-6 h-6 inline-flex items-center justify-center text-white text-xs">SB</span>
                            synapsbranch
                        </h1>
                    </div>
                </div>

                <div className="flex items-center gap-4">
                    <ThemeToggle />

                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="relative h-9 w-9 rounded-full border border-border/50 pl-0 pr-0">
                                <Avatar className="h-9 w-9">
                                    <AvatarImage src={user?.avatar_url} alt={user?.name || "User"} />
                                    <AvatarFallback className="bg-brand-500/10 text-brand-500 text-xs font-medium">
                                        {user?.name ? getInitials(user.name) : "US"}
                                    </AvatarFallback>
                                </Avatar>
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent className="w-56" align="end" forceMount>
                            <DropdownMenuLabel className="font-normal">
                                <div className="flex flex-col space-y-1">
                                    <p className="text-sm font-medium leading-none">{user?.name || "User"}</p>
                                    <p className="text-xs leading-none text-muted-foreground">
                                        {user?.email || "user@example.com"}
                                    </p>
                                </div>
                            </DropdownMenuLabel>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem asChild>
                                <Link href="/settings" className="cursor-pointer flex items-center">
                                    <UserIcon className="mr-2 h-4 w-4" />
                                    <span>Profil</span>
                                </Link>
                            </DropdownMenuItem>
                            <DropdownMenuItem asChild>
                                <Link href="/settings" className="cursor-pointer flex items-center">
                                    <Settings className="mr-2 h-4 w-4" />
                                    <span>Paramètres</span>
                                </Link>
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem onClick={handleLogout} className="cursor-pointer text-red-500 focus:text-red-500">
                                <LogOut className="mr-2 h-4 w-4" />
                                <span>Déconnexion</span>
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </div>
            </div>
        </header>
    );
}
