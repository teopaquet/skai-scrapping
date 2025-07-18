import { useState, useCallback, useRef, useEffect } from 'react';
import api from '../services/api';
import { cache, createCacheKey } from '../utils/cache';

interface UseOptimizedApiOptions {
    cacheTime?: number; // in milliseconds
    enabled?: boolean;
    onSuccess?: (data: any) => void;
    onError?: (error: any) => void;
}

interface UseOptimizedApiResult<T> {
    data: T | null;
    loading: boolean;
    error: Error | null;
    refetch: () => Promise<void>;
    mutate: (endpoint: string, data?: any, method?: 'POST' | 'PUT' | 'DELETE') => Promise<any>;
}

export function useOptimizedApi<T = any>(
    endpoint: string,
    params: Record<string, any> = {},
    options: UseOptimizedApiOptions = {}
): UseOptimizedApiResult<T> {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);
    const abortControllerRef = useRef<AbortController | null>(null);
    
    const { cacheTime = 5 * 60 * 1000, enabled = true, onSuccess, onError } = options;
    
    const fetchData = useCallback(async () => {
        if (!enabled) return;
        
        const cacheKey = createCacheKey(endpoint, params);
        
        // Check cache first
        const cachedData = cache.get<T>(cacheKey);
        if (cachedData) {
            setData(cachedData);
            setError(null);
            onSuccess?.(cachedData);
            return;
        }
        
        // Cancel previous request
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }
        
        abortControllerRef.current = new AbortController();
        setLoading(true);
        setError(null);
        
        try {
            const queryString = Object.keys(params)
                .map(key => `${key}=${encodeURIComponent(params[key])}`)
                .join('&');
            const url = `${endpoint}${queryString ? `?${queryString}` : ''}`;
            
            const response = await api.get(url, {
                signal: abortControllerRef.current.signal
            });
            
            const responseData = response.data;
            setData(responseData);
            
            // Cache the response
            cache.set(cacheKey, responseData, cacheTime);
            
            onSuccess?.(responseData);
        } catch (err: any) {
            if (err.name !== 'AbortError') {
                const error = new Error(err.message || 'An error occurred');
                setError(error);
                onError?.(error);
            }
        } finally {
            setLoading(false);
        }
    }, [endpoint, JSON.stringify(params), enabled, cacheTime, onSuccess, onError]);
    
    const mutate = useCallback(async (
        mutateEndpoint: string, 
        mutateData?: any, 
        method: 'POST' | 'PUT' | 'DELETE' = 'POST'
    ) => {
        setLoading(true);
        try {
            let response;
            switch (method) {
                case 'POST':
                    response = await api.post(mutateEndpoint, mutateData);
                    break;
                case 'PUT':
                    response = await api.put(mutateEndpoint, mutateData);
                    break;
                case 'DELETE':
                    response = await api.delete(mutateEndpoint);
                    break;
            }
            
            // Clear related cache entries
            cache.clear(endpoint.split('?')[0]);
            
            return response.data;
        } catch (err: any) {
            throw new Error(err.message || 'Mutation failed');
        } finally {
            setLoading(false);
        }
    }, [endpoint]);
    
    useEffect(() => {
        fetchData();
        
        // Cleanup function
        return () => {
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, [fetchData]);
    
    return {
        data,
        loading,
        error,
        refetch: fetchData,
        mutate
    };
}

// Debounce hook for search inputs
export function useDebounce<T>(value: T, delay: number): T {
    const [debouncedValue, setDebouncedValue] = useState<T>(value);

    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => {
            clearTimeout(handler);
        };
    }, [value, delay]);

    return debouncedValue;
}
