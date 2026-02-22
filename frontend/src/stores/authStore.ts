import { create } from 'zustand';
import { api } from '@/lib/api';
import { User, LoginRequest, RegisterRequest, TokenResponse } from '@/types/auth';

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (data: LoginRequest) => Promise<void>;
    register: (data: RegisterRequest) => Promise<string>;
    logout: () => void;
    fetchUser: () => Promise<void>;
    hydrate: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
    user: null,
    isAuthenticated: false,
    isLoading: true,

    hydrate: () => {
        if (typeof window !== 'undefined') {
            const tokens = localStorage.getItem('auth_tokens');
            if (tokens) {
                set({ isAuthenticated: true });
            } else {
                set({ isAuthenticated: false, isLoading: false });
            }
        }
    },

    login: async (data: LoginRequest) => {
        set({ isLoading: true });
        try {
            const params = new URLSearchParams();
            params.append('username', data.email);
            params.append('password', data.password || '');

            const response = await api.post<TokenResponse>('/auth/login', params, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            localStorage.setItem('auth_tokens', JSON.stringify(response.data));
            set({ isAuthenticated: true });
            await useAuthStore.getState().fetchUser();
        } catch (error) {
            set({ isAuthenticated: false, isLoading: false });
            throw error;
        }
    },

    register: async (data: RegisterRequest) => {
        set({ isLoading: true });
        try {
            const response = await api.post('/auth/register', data);
            set({ isLoading: false });
            return response.data?.message || 'Inscription réussie';
        } catch (error) {
            set({ isLoading: false });
            throw error;
        }
    },

    logout: async () => {
        try {
            await api.post('/auth/logout');
        } catch (e) { }
        localStorage.removeItem('auth_tokens');
        set({ user: null, isAuthenticated: false, isLoading: false });
    },

    fetchUser: async () => {
        try {
            const response = await api.get<User>('/users/me');
            set({ user: response.data, isAuthenticated: true, isLoading: false });
        } catch (error) {
            localStorage.removeItem('auth_tokens');
            set({ user: null, isAuthenticated: false, isLoading: false });
            throw error;
        }
    }
}));
