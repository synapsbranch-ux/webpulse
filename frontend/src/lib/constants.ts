export const PHASES = [
    { id: 'dns', label: 'DNS' },
    { id: 'ssl', label: 'SSL' },
    { id: 'performance', label: 'PERF' },
    { id: 'dast', label: 'DAST' },
    { id: 'seo', label: 'SEO' },
];

export const SEVERITY_LEVELS = {
    critical: 'Critique',
    high: 'Élevé',
    medium: 'Moyen',
    low: 'Faible',
};

export const GRADE_COLORS = {
    'A+': 'text-green-500 bg-green-500/10 border-green-500/20',
    'A': 'text-green-400 bg-green-400/10 border-green-400/20',
    'B': 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20',
    'C': 'text-orange-500 bg-orange-500/10 border-orange-500/20',
    'D': 'text-red-500 bg-red-500/10 border-red-500/20',
    'F': 'text-red-600 bg-red-600/10 border-red-600/20',
};

export const ROUTES = {
    HOME: '/',
    LOGIN: '/login',
    REGISTER: '/register',
    DASHBOARD: '/dashboard',
    NEW_SCAN: '/new-scan',
    HISTORY: '/history',
    SETTINGS: '/settings',
};
