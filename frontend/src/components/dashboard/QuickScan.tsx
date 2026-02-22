"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Globe, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function QuickScan() {
    const [url, setUrl] = useState("");
    const router = useRouter();

    const handleScan = (e: React.FormEvent) => {
        e.preventDefault();
        if (url) {
            router.push(`/new-scan?url=${encodeURIComponent(url)}`);
        }
    };

    return (
        <div className="rounded-xl border border-brand-500/20 bg-brand-500/5 p-6 backdrop-blur-sm">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h3 className="text-lg font-semibold text-foreground">Scan Rapide</h3>
                    <p className="text-sm text-muted-foreground">Analysez un nouveau domaine instantanément</p>
                </div>
                <form onSubmit={handleScan} className="flex flex-1 max-w-lg gap-3">
                    <div className="relative flex-1">
                        <Globe className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                        <Input
                            type="url"
                            placeholder="https://example.com"
                            required
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            className="pl-9 bg-background"
                        />
                    </div>
                    <Button type="submit" className="bg-brand-500 hover:bg-brand-600 transition-colors">
                        Lancer <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                </form>
            </div>
        </div>
    );
}
