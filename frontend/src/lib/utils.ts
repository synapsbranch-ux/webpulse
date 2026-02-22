import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import { format, parseISO } from "date-fns"
import { fr } from "date-fns/locale"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(dateString: string, pattern: string = "dd MMM yyyy, HH:mm") {
  if (!dateString) return "";
  try {
    return format(parseISO(dateString), pattern, { locale: fr });
  } catch (e) {
    return dateString;
  }
}

export function formatScore(score: number | undefined | null) {
  if (score === null || score === undefined) return "N/A";
  return `${Math.round(score)}/100`;
}

export function getGradeColor(grade: string | undefined): string {
  if (!grade) return 'text-muted-foreground bg-muted/50 border-border';
  switch (grade.toUpperCase()) {
    case 'A+': return 'text-green-500 bg-green-500/10 border-green-500/20';
    case 'A': return 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20';
    case 'B': return 'text-blue-500 bg-blue-500/10 border-blue-500/20';
    case 'C': return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20';
    case 'D': return 'text-orange-500 bg-orange-500/10 border-orange-500/20';
    case 'F': default: return 'text-red-500 bg-red-500/10 border-red-500/20';
  }
}
