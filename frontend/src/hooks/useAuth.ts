import { useEffect } from 'react';
import { useAuthStore } from '@/stores/authStore';

export function useAuth() {
    const { user, isAuthenticated, isLoading, login, register, logout, fetchUser, hydrate } = useAuthStore();

    useEffect(() => {
        hydrate();
        if (typeof window !== 'undefined' && localStorage.getItem('auth_tokens') && !user) {
            fetchUser().catch(() => { });
        }
    }, [hydrate, fetchUser, user]);

    return { user, isAuthenticated, isLoading, login, register, logout, fetchUser };
}

