import Link from "next/link";
import { Hero } from "@/components/landing/Hero";
import { Features } from "@/components/landing/Features";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { Pricing } from "@/components/landing/Pricing";
import { Footer } from "@/components/landing/Footer";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Public Header */}
      <header className="fixed top-0 z-50 w-full border-b border-white/5 bg-background/80 backdrop-blur-md">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <span className="bg-brand-500 rounded-md w-7 h-7 inline-flex items-center justify-center text-white text-xs font-bold shadow-lg shadow-brand-500/20">SB</span>
            <span className="font-bold text-xl tracking-tight">synapsbranch</span>
          </Link>
          <div className="flex items-center gap-4">
            <Link href="/login" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors hidden sm:block">
              Se connecter
            </Link>
            <Button asChild className="rounded-full shadow-lg shadow-brand-500/10">
              <Link href="/register">Commencer gratuitement</Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1">
        <Hero />
        <Features />
        <HowItWorks />
        <Pricing />
      </main>

      <Footer />
    </div>
  );
}
