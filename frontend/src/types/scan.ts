export type ScanStatus = 'pending' | 'running' | 'completed' | 'failed';

export interface Scan {
    id: string;
    url: string;
    status: ScanStatus;
    current_phase?: string;
    overall_score?: number;
    started_at?: string;
    completed_at?: string;
    duration_seconds?: number;
    created_at: string;
}

export interface ScanResult {
    id: string;
    module: string;
    score: number;
    grade: string;
    data: any;
    issues_critical: number;
    issues_high: number;
    issues_medium: number;
    issues_low: number;
}

export interface LogEntry {
    timestamp: string;
    phase: string;
    level: 'success' | 'warning' | 'error' | 'info';
    message: string;
}

export interface LiveMetrics {
    avg_response_time: number;
    throughput: number;
    error_rate: number;
    active_users: number;
}

export type WSMessage = {
    type: 'phase_change' | 'log' | 'progress' | 'module_complete' | 'scan_complete' | 'report_ready' | 'error';
    [key: string]: any;
};
