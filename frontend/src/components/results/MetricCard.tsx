"use client";

import { LucideIcon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

interface MetricCardProps {
    title: string;
    value: string | number;
    icon: LucideIcon;
    description?: string;
    trend?: {
        value: number;
        isPositive: boolean;
    };
    isLoading?: boolean;
}

export function MetricCard({ title, value, icon: Icon, description, trend, isLoading }: MetricCardProps) {
    if (isLoading) {
        return (
            <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
                <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                        <Skeleton className="h-4 w-24" />
                        <Skeleton className="h-8 w-8 rounded-full" />
                    </div>
                    <Skeleton className="h-8 w-16 mb-2" />
                    <Skeleton className="h-3 w-32" />
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className="border-border/50 bg-card/50 backdrop-blur-sm overflow-hidden relative group">
            <div className="absolute inset-x-0 bottom-0 h-1 bg-gradient-to-r from-transparent via-brand-500/20 to-transparent scale-x-0 group-hover:scale-x-100 transition-transform duration-500" />
            <CardContent className="p-6">
                <div className="flex items-center justify-between space-y-0 pb-2">
                    <p className="text-sm font-medium text-muted-foreground">{title}</p>
                    <div className="p-2 bg-brand-500/10 rounded-lg text-brand-500">
                        <Icon className="h-4 w-4" />
                    </div>
                </div>
                <div className="flex flex-col gap-1">
                    <div className="text-2xl font-bold tracking-tight">{value}</div>
                    {description && (
                        <p className="text-xs text-muted-foreground">
                            {description}
                        </p>
                    )}
                    {trend && (
                        <div className={`flex items-center text-xs mt-1 font-medium ${trend.isPositive ? 'text-emerald-500' : 'text-red-500'}`}>
                            <span className="flex items-center">
                                {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}%
                            </span>
                            <span className="text-muted-foreground ml-1">vs moyenne</span>
                        </div>
                    )}
                </div>
            </CardContent>
        </Card>
    );
}
