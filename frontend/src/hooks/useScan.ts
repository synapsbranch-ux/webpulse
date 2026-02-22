import { useCallback, useState } from 'react';
import { api } from '@/lib/api';
import { useScanStore } from '@/stores/scanStore';
import { Scan } from '@/types/scan';

export function useScan() {
    const { setCurrentScan, reset } = useScanStore();
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const startScan = useCallback(async (url: string) => {
        setIsLoading(true);
        setError(null);
        try {
            reset();
            const response = await api.post<Scan>('/scans', { url });
            setCurrentScan(response.data);
            return response.data;
        } catch (e: any) {
            setError(e?.response?.data?.detail || e.message || 'Erreur lors du lancement');
            throw e;
        } finally {
            setIsLoading(false);
        }
    }, [reset, setCurrentScan]);

    const getScan = useCallback(async (id: string) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await api.get<Scan>(`/scans/${id}`);
            setCurrentScan(response.data);
            return response.data;
        } catch (e: any) {
            setError(e?.response?.data?.detail || e.message || 'Erreur lors de la récupération');
            throw e;
        } finally {
            setIsLoading(false);
        }
    }, [setCurrentScan]);

    const getScans = useCallback(async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await api.get<Scan[]>('/scans');
            return response.data;
        } catch (e: any) {
            setError(e?.response?.data?.detail || e.message);
            throw e;
        } finally {
            setIsLoading(false);
        }
    }, []);

    const deleteScan = useCallback(async (id: string) => {
        setIsLoading(true);
        setError(null);
        try {
            await api.delete(`/scans/${id}`);
        } catch (e: any) {
            setError(e?.response?.data?.detail || e.message);
            throw e;
        } finally {
            setIsLoading(false);
        }
    }, []);

    return { startScan, getScan, getScans, deleteScan, isLoading, error };
}
