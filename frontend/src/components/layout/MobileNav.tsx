"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, LayoutDashboard, History, Settings, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger, SheetTitle } from "@/components/ui/sheet";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/new-scan", label: "Nouveau Scan", icon: Zap },
    { href: "/history", label: "Historique", icon: History },
    { href: "/settings", label: "Paramètres", icon: Settings },
];

export function MobileNav() {
    const [open, setOpen] = React.useState(false);
    const pathname = usePathname();

    return (
        <Sheet open={open} onOpenChange={setOpen}>
            <SheetTrigger asChild>
                <Button
                    variant="ghost"
                    className="mr-2 px-0 text-base hover:bg-transparent focus-visible:bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 sm:hidden"
                >
                    <Menu className="h-6 w-6" />
                    <span className="sr-only">Toggle Menu</span>
                </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-[280px] pr-0">
                <SheetTitle className="sr-only">Menu de Navigation</SheetTitle>
                <div className="flex flex-col h-full py-4">
                    <Link
                        href="/dashboard"
                        className="flex items-center gap-2 mb-8 px-4"
                        onClick={() => setOpen(false)}
                    >
                        <span className="bg-brand-500 rounded-md w-6 h-6 inline-flex items-center justify-center text-white text-xs font-bold">SB</span>
                        <span className="font-bold text-xl tracking-tight">synapsbranch</span>
                    </Link>
                    <nav className="flex flex-col gap-2">
                        {NAV_ITEMS.map((item) => {
                            const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
                            const Icon = item.icon;
                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    onClick={() => setOpen(false)}
                                    className={cn(
                                        "flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors mx-2",
                                        isActive
                                            ? "bg-brand-500/10 text-brand-500"
                                            : "text-muted-foreground hover:bg-muted hover:text-foreground"
                                    )}
                                >
                                    <Icon className="h-5 w-5" />
                                    {item.label}
                                </Link>
                            );
                        })}
                    </nav>
                </div>
            </SheetContent>
        </Sheet>
    );
}
