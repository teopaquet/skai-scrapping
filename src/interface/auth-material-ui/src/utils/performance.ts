// Performance testing utilities
export const performanceMonitor = {
    // Measure component render time
    measureRender: (componentName: string, renderFn: () => void) => {
        const start = performance.now();
        renderFn();
        const end = performance.now();
        console.log(`${componentName} render time: ${end - start}ms`);
    },

    // Measure API call time
    measureApiCall: async (apiCall: () => Promise<any>, name: string) => {
        const start = performance.now();
        try {
            const result = await apiCall();
            const end = performance.now();
            console.log(`${name} API call time: ${end - start}ms`);
            return result;
        } catch (error) {
            const end = performance.now();
            console.log(`${name} API call failed after: ${end - start}ms`);
            throw error;
        }
    },

    // Memory usage monitoring
    logMemoryUsage: (label: string) => {
        if ('memory' in performance) {
            const memory = (performance as any).memory;
            console.log(`${label} - Memory Usage:`, {
                used: `${Math.round(memory.usedJSHeapSize / 1048576)} MB`,
                total: `${Math.round(memory.totalJSHeapSize / 1048576)} MB`,
                limit: `${Math.round(memory.jsHeapSizeLimit / 1048576)} MB`
            });
        }
    },

    // Track re-renders
    trackRenders: (componentName: string) => {
        let renderCount = 0;
        return () => {
            renderCount++;
            console.log(`${componentName} rendered ${renderCount} times`);
        };
    }
};
