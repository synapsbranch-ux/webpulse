"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { Sidebar } from "@/components/layout/Sidebar";
import { Header } from "@/components/layout/Header";
import { Skeleton } from "@/components/ui/skeleton";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const { isAuthenticated, isLoading, fetchUser } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isLoading && !isAuthenticated) {
            router.push('/login');
        }
    }, [isLoading, isAuthenticated, router]);

    if (isLoading || !isAuthenticated) {
        return (
            <div className="flex min-h-screen w-full flex-col bg-background">
                <header className="sticky top-0 z-40 w-full border-b border-border/50 bg-background/80 h-16 flex items-center px-4 sm:px-6 justify-between">
                    <Skeleton className="h-8 w-48" />
                    <Skeleton className="h-9 w-9 rounded-full" />
                </header>
                <div className="flex flex-1">
                    <aside className="hidden sm:block border-r border-sidebar-border w-64 p-4">
                        <div className="space-y-4">
                            <Skeleton className="h-10 w-full" />
                            <Skeleton className="h-10 w-full" />
                            <Skeleton className="h-10 w-full" />
                        </div>
                    </aside>
                    <main className="flex-1 p-6">
                        <div className="space-y-6">
                            <Skeleton className="h-[200px] w-full rounded-xl" />
                            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                                <Skeleton className="h-[120px] rounded-xl" />
                                <Skeleton className="h-[120px] rounded-xl" />
                                <Skeleton className="h-[120px] rounded-xl" />
                                <Skeleton className="h-[120px] rounded-xl" />
                            </div>
                        </div>
                    </main>
                </div>
            </div>
        );
    }

    return (
        <div className="flex min-h-screen w-full flex-col bg-background">
            <Header />
            <div className="flex flex-1 overflow-hidden">
                <Sidebar className="hidden sm:flex" />
                <main className="flex-1 overflow-y-auto w-full p-4 sm:p-6 lg:p-8">
                    <div className="mx-auto max-w-7xl">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
}
