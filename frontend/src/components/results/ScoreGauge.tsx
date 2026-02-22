"use client";

import { motion } from "framer-motion";
import { getGradeColor } from "@/lib/utils";

interface ScoreGaugeProps {
    score: number;
    label?: string;
    size?: number;
    strokeWidth?: number;
}

export function ScoreGauge({
    score,
    label = "Score",
    size = 180,
    strokeWidth = 12
}: ScoreGaugeProps) {
    const radius = (size - strokeWidth) / 2;
    const circumference = radius * 2 * Math.PI;
    const strokeDashoffset = circumference - (score / 100) * circumference;

    const getGrade = (s: number) => {
        if (s >= 90) return "A";
        if (s >= 80) return "B";
        if (s >= 70) return "C";
        if (s >= 60) return "D";
        return "F";
    };

    const gradeLetter = getGrade(score);
    const colorClass = getGradeColor(gradeLetter);
    // Extrait la couleur de la classe Tailwind si possible (simplifié ici par des hex)
    let strokeColor = "#3b82f6"; // default blue
    if (colorClass.includes("emerald")) strokeColor = "#10b981";
    else if (colorClass.includes("amber")) strokeColor = "#f59e0b";
    else if (colorClass.includes("red")) strokeColor = "#ef4444";

    return (
        <div className="relative flex flex-col items-center justify-center" style={{ width: size, height: size }}>
            <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="transform -rotate-90">
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke="currentColor"
                    strokeWidth={strokeWidth}
                    fill="transparent"
                    className="text-muted/20"
                />
                <motion.circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    stroke={strokeColor}
                    strokeWidth={strokeWidth}
                    strokeLinecap="round"
                    fill="transparent"
                    strokeDasharray={circumference}
                    initial={{ strokeDashoffset: circumference }}
                    animate={{ strokeDashoffset }}
                    transition={{ duration: 1.5, ease: "easeOut" }}
                />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
                <motion.span
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.5 }}
                    className="text-5xl font-black tracking-tighter"
                >
                    {gradeLetter}
                </motion.span>
                <span className="text-sm font-medium text-muted-foreground mt-1">
                    {score}/100
                </span>
            </div>
            {label && (
                <div className="absolute -bottom-8 text-center text-sm font-semibold uppercase tracking-wider text-muted-foreground w-full">
                    {label}
                </div>
            )}
        </div>
    );
}
