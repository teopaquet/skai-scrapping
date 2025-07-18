// Simple cache utility to reduce API calls and improve performance
interface CacheItem<T> {
    data: T;
    timestamp: number;
    ttl: number; // Time to live in milliseconds
}

class SimpleCache {
    private cache = new Map<string, CacheItem<any>>();
    private defaultTTL = 5 * 60 * 1000; // 5 minutes default

    set<T>(key: string, data: T, ttl: number = this.defaultTTL): void {
        this.cache.set(key, {
            data,
            timestamp: Date.now(),
            ttl
        });
    }

    get<T>(key: string): T | null {
        const item = this.cache.get(key);
        if (!item) return null;

        const now = Date.now();
        if (now - item.timestamp > item.ttl) {
            this.cache.delete(key);
            return null;
        }

        return item.data;
    }

    clear(keyPattern?: string): void {
        if (!keyPattern) {
            this.cache.clear();
            return;
        }

        for (const key of this.cache.keys()) {
            if (key.includes(keyPattern)) {
                this.cache.delete(key);
            }
        }
    }

    has(key: string): boolean {
        const item = this.cache.get(key);
        if (!item) return false;

        const now = Date.now();
        if (now - item.timestamp > item.ttl) {
            this.cache.delete(key);
            return false;
        }

        return true;
    }
}

export const cache = new SimpleCache();

// Helper function to create cache keys
export const createCacheKey = (endpoint: string, params: Record<string, any> = {}): string => {
    const paramString = Object.keys(params)
        .sort()
        .map(key => `${key}=${params[key]}`)
        .join('&');
    return `${endpoint}${paramString ? `?${paramString}` : ''}`;
};
