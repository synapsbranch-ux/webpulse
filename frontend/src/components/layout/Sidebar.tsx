"use client";

import Link from "Link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, History, Settings, Zap, ShieldAlert, BarChart3, Clock, Target } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
    { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/new-scan", label: "Nouveau Scan", icon: Zap },
    { href: "/history", label: "Historique", icon: History },
];

const SECONDARY_NAV_ITEMS = [
    { href: "/settings", label: "Paramètres", icon: Settings },
];

export function Sidebar({ className }: { className?: string }) {
    const pathname = usePathname();

    return (
        <aside className={cn("flex flex-col border-r border-sidebar-border bg-sidebar/50 backdrop-blur-md w-64 min-h-[calc(100vh-4rem)] p-4", className)}>
            <div className="space-y-6 flex-1">
                <div className="space-y-1">
                    <h4 className="px-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-4">
                        Navigation
                    </h4>
                    <nav className="space-y-1">
                        {NAV_ITEMS.map((item) => {
                            const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
                            const Icon = item.icon;
                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={cn(
                                        "flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all duration-200",
                                        isActive
                                            ? "bg-brand-500/10 text-brand-500 shadow-sm border border-brand-500/20"
                                            : "text-muted-foreground hover:bg-muted hover:text-foreground"
                                    )}
                                >
                                    <Icon className={cn("h-5 w-5", isActive && "text-brand-500")} />
                                    {item.label}
                                </Link>
                            );
                        })}
                    </nav>
                </div>
            </div>

            <div className="mt-auto space-y-1 pt-6 border-t border-border/50">
                <nav className="space-y-1">
                    {SECONDARY_NAV_ITEMS.map((item) => {
                        const isActive = pathname === item.href || pathname.startsWith(item.href);
                        const Icon = item.icon;
                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={cn(
                                    "flex items-center gap-3 rounded-lg px-4 py-2.5 text-sm font-medium transition-colors",
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
        </aside>
    );
}
