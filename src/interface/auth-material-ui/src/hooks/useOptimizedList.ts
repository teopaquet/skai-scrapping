import { useState, useCallback, useEffect, useMemo } from 'react';
import { optimizedAPI } from '../api/optimizedAPI';
import { useDebounce } from './useOptimizedApi';

interface UseOptimizedListOptions {
    pageSize?: number;
    enablePagination?: boolean;
    cacheTime?: number;
    autoFetch?: boolean;
    dependencies?: any[];
}

interface UseOptimizedListResult<T> {
    data: T[];
    loading: boolean;
    error: Error | null;
    page: number;
    pageSize: number;
    rowCount: number;
    selectedRows: string[];
    
    // Actions
    setPage: (page: number) => void;
    setPageSize: (size: number) => void;
    setSelectedRows: (rows: string[]) => void;
    refetch: () => Promise<void>;
    deleteSelected: () => Promise<void>;
    deleteItem: (id: string | number) => Promise<void>;
    
    // Handlers for DataGrid
    handlePaginationChange: (params: { page: number; pageSize: number }) => void;
    handleRowSelectionChange: (selection: any) => void;
}

export function useOptimizedList<T = any>(
    endpoint: string,
    options: UseOptimizedListOptions = {}
): UseOptimizedListResult<T> {
    const {
        pageSize: initialPageSize = 15,
        enablePagination = true,
        cacheTime = 5 * 60 * 1000,
        autoFetch = true,
        dependencies = []
    } = options;

    // State
    const [data, setData] = useState<T[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);
    const [page, setPage] = useState(0);
    const [pageSize, setPageSize] = useState(initialPageSize);
    const [rowCount, setRowCount] = useState(0);
    const [selectedRows, setSelectedRows] = useState<string[]>([]);

    // Debounce pagination to reduce API calls
    const debouncedPage = useDebounce(page, 300);
    const debouncedPageSize = useDebounce(pageSize, 300);

    // Fetch data function
    const fetchData = useCallback(async () => {
        setLoading(true);
        setError(null);

        try {
            const params: any = {
                sort_by: 'id',
                sort_order: 'asc'
            };

            if (enablePagination) {
                params.page = debouncedPage + 1;
                params.limit = debouncedPageSize;
            } else {
                params.limit = 1000; // Large limit for non-paginated lists
            }

            const response = await optimizedAPI.get(endpoint, { params });
            
            const responseData = response.data as any;
            const items = Array.isArray(responseData) ? responseData : responseData.items || [];
            
            setData(items);
            setRowCount(responseData.total || items.length);
        } catch (err: any) {
            setError(new Error(err.message || 'Failed to fetch data'));
            setData([]);
            setRowCount(0);
        } finally {
            setLoading(false);
        }
    }, [endpoint, debouncedPage, debouncedPageSize, enablePagination, ...dependencies]);

    // Auto-fetch on mount and dependency changes
    useEffect(() => {
        if (autoFetch) {
            fetchData();
        }
    }, [fetchData, autoFetch]);

    // Delete selected items
    const deleteSelected = useCallback(async () => {
        if (selectedRows.length === 0) return;

        if (!window.confirm(`Are you sure you want to delete ${selectedRows.length} item(s)?`)) {
            return;
        }

        setLoading(true);
        try {
            await Promise.all(
                selectedRows.map(id => optimizedAPI.delete(`${endpoint}/${id}`))
            );
            setSelectedRows([]);
            await fetchData();
        } catch (err: any) {
            setError(new Error(err.message || 'Failed to delete items'));
            throw err;
        } finally {
            setLoading(false);
        }
    }, [selectedRows, endpoint, fetchData]);

    // Delete single item
    const deleteItem = useCallback(async (id: string | number) => {
        if (!window.confirm('Are you sure you want to delete this item?')) {
            return;
        }

        setLoading(true);
        try {
            await optimizedAPI.delete(`${endpoint}/${id}`);
            await fetchData();
        } catch (err: any) {
            setError(new Error(err.message || 'Failed to delete item'));
            throw err;
        } finally {
            setLoading(false);
        }
    }, [endpoint, fetchData]);

    // Memoized handlers
    const handlePaginationChange = useCallback((params: { page: number; pageSize: number }) => {
        setPage(params.page);
        setPageSize(params.pageSize);
    }, []);

    const handleRowSelectionChange = useCallback((selection: any) => {
        const selectedIds = Array.isArray(selection) ? selection : [];
        setSelectedRows(selectedIds.map(String));
    }, []);

    return {
        data,
        loading,
        error,
        page,
        pageSize,
        rowCount,
        selectedRows,
        
        setPage,
        setPageSize,
        setSelectedRows,
        refetch: fetchData,
        deleteSelected,
        deleteItem,
        
        handlePaginationChange,
        handleRowSelectionChange
    };
}
