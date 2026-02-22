import axios from 'axios';
import { TokenResponse } from '@/types/auth';

const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: `${baseURL}/api/v1`,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    (config) => {
        if (typeof window !== 'undefined') {
            const tokensStr = localStorage.getItem('auth_tokens');
            if (tokensStr) {
                try {
                    const tokens: TokenResponse = JSON.parse(tokensStr);
                    if (tokens.access_token) {
                        config.headers.Authorization = `Bearer ${tokens.access_token}`;
                    }
                } catch (e) {
                    // Tokens malformed
                }
            }
        }
        return config;
    },
    (error) => Promise.reject(error)
);

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response?.status === 401 && !originalRequest._retry && typeof window !== 'undefined') {
            originalRequest._retry = true;
            try {
                const tokensStr = localStorage.getItem('auth_tokens');
                if (tokensStr) {
                    const tokens: TokenResponse = JSON.parse(tokensStr);
                    const response = await axios.post(`${baseURL}/api/v1/auth/refresh`, {
                        refresh_token: tokens.refresh_token,
                    });
                    const newTokens: TokenResponse = response.data;
                    localStorage.setItem('auth_tokens', JSON.stringify(newTokens));
                    originalRequest.headers.Authorization = `Bearer ${newTokens.access_token}`;
                    return api(originalRequest);
                }
            } catch (refreshError) {
                localStorage.removeItem('auth_tokens');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);
