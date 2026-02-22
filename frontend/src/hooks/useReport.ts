import { useCallback, useState } from 'react';
import { api } from '@/lib/api';
import { Report } from '@/types/report';

export function useReport(scanId: string) {
    const [report, setReport] = useState<Report | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const getReport = useCallback(async () => {
        if (!scanId) return null;
        setIsLoading(true);
        setError(null);
        try {
            const response = await api.get<Report>(`/reports/${scanId}`);
            setReport(response.data);
            return response.data;
        } catch (e: any) {
            setError(e?.response?.data?.detail || e.message || 'Erreur chargement rapport');
            throw e;
        } finally {
            setIsLoading(false);
        }
    }, [scanId]);

    const downloadPdf = useCallback(async () => {
        if (!scanId) return;
        try {
            const response = await api.get(`/reports/${scanId}/pdf`, {
                responseType: 'blob',
            });
            const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `report-${scanId}.pdf`);
            document.body.appendChild(link);
            link.click();
            if (link.parentNode) link.parentNode.removeChild(link);
        } catch (e) {
            throw new Error('Erreur de téléchargement du PDF');
        }
    }, [scanId]);

    const sendEmail = useCallback(async (email: string) => {
        if (!scanId) return;
        try {
            await api.post(`/reports/${scanId}/email`, { email });
        } catch (e) {
            throw new Error("Erreur d'envoi du rapport");
        }
    }, [scanId]);

    return { report, isLoading, error, getReport, downloadPdf, sendEmail };
}
