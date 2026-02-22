import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Github } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-background relative overflow-hidden">
      {/* Background gradients for aesthetics */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <div className="absolute -top-1/4 -right-1/4 w-[800px] h-[800px] bg-brand-500/10 rounded-full blur-[120px]" />
        <div className="absolute -bottom-1/4 -left-1/4 w-[800px] h-[800px] bg-emerald-500/10 rounded-full blur-[120px]" />
      </div>

      <main className="z-10 bg-card/50 border border-border/50 backdrop-blur-xl p-8 md:p-12 rounded-3xl shadow-2xl max-w-2xl w-full flex flex-col items-center text-center space-y-8">

        {/* Logos Container */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-8 sm:gap-16 w-full">
          <div className="relative w-32 h-32 md:w-40 md:h-40 shrink-0">
            <Image
              src="/assets/logoisteah.jpg"
              alt="Logo ISTeAH"
              fill
              className="object-contain"
            />
          </div>
          <div className="relative w-40 h-40 md:w-48 md:h-48 shrink-0">
            <Image
              src="/assets/synapsbranch.png"
              alt="Logo Synapsbranch"
              fill
              className="object-contain"
            />
          </div>
        </div>

        <div className="space-y-4">
          <h1 className="text-3xl md:text-5xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/70">
            Synapsbranch
          </h1>
          <p className="text-xl md:text-2xl text-muted-foreground font-medium">
            Analyseur de Sécurité et Performance Web
          </p>
        </div>

        <div className="p-4 bg-muted/50 rounded-xl border border-white/5 w-full">
          <p className="text-sm md:text-base text-muted-foreground">
            Ce projet est réalisé dans le cadre du cours universitaire <strong className="text-foreground">LOG2000</strong>.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 w-full pt-4">
          <Button asChild size="lg" variant="outline" className="w-full sm:w-auto min-w-[160px] rounded-full">
            <Link href="/login">Se Connecter</Link>
          </Button>
          <Button asChild size="lg" className="w-full sm:w-auto min-w-[160px] rounded-full shadow-lg shadow-brand-500/20">
            <Link href="/register">S'inscrire</Link>
          </Button>
        </div>

      </main>

      <footer className="z-10 mt-12 flex flex-col items-center gap-4 text-sm text-muted-foreground">
        <div>
          &copy; {new Date().getFullYear()} Synapsbranch. Distribué sous <a href="https://opensource.org/licenses/MIT" target="_blank" rel="noopener noreferrer" className="underline hover:text-foreground transition-colors">Licence MIT</a>.
        </div>
        <a
          href="https://github.com/synapsbranch-ux/webpulse.git"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 hover:text-foreground transition-colors"
        >
          <Github className="w-4 h-4" />
          <span>synapsbranch-ux/webpulse</span>
        </a>
      </footer>
    </div>
  );
}

