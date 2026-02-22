import { Scan } from "./scan";

export interface Report {
    id: string;
    scan_id: string;
    scan: Scan;
    ai_analysis: AIAnalysis | null;
    pdf_path: string | null;
    created_at: string;
    overall_score?: number;
    module_scores?: Record<string, number>;
    issues?: Issue[];
}

export interface AIAnalysis {
    executive_summary: string;
    overall_score: number;
    scores_by_category: Record<string, number>;
    critical_issues: Issue[];
    warnings: Issue[];
    recommendations: Recommendation[];
    performance_analysis: string;
    security_analysis: string;
    seo_analysis: string;
}

export interface Issue {
    title: string;
    description: string;
    category: string;
    severity: string;  // 'critical', 'high', 'medium', 'low', 'info'
    solution: string;
}

export interface Recommendation {
    priority: 'high' | 'medium' | 'low';
    title: string;
    description: string;
    impact: string;
}

