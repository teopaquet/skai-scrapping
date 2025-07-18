import React, { createContext, useContext, useReducer, useCallback, useEffect } from 'react';

// Global state interface
interface GlobalState {
    airlines: any[];
    currentUser: any | null;
    theme: 'light' | 'dark';
    loading: {
        airlines: boolean;
        user: boolean;
    };
    cache: {
        lastFetch: Record<string, number>;
    };
}

// Action types
type GlobalAction =
    | { type: 'SET_AIRLINES'; payload: any[] }
    | { type: 'SET_CURRENT_USER'; payload: any }
    | { type: 'SET_THEME'; payload: 'light' | 'dark' }
    | { type: 'SET_LOADING'; payload: { key: keyof GlobalState['loading']; value: boolean } }
    | { type: 'SET_LAST_FETCH'; payload: { key: string; timestamp: number } }
    | { type: 'CLEAR_CACHE' };

// Initial state
const initialState: GlobalState = {
    airlines: [],
    currentUser: null,
    theme: 'light',
    loading: {
        airlines: false,
        user: false,
    },
    cache: {
        lastFetch: {},
    },
};

// Reducer
function globalReducer(state: GlobalState, action: GlobalAction): GlobalState {
    switch (action.type) {
        case 'SET_AIRLINES':
            return {
                ...state,
                airlines: action.payload,
                loading: { ...state.loading, airlines: false },
            };
        case 'SET_CURRENT_USER':
            return {
                ...state,
                currentUser: action.payload,
                loading: { ...state.loading, user: false },
            };
        case 'SET_THEME':
            return {
                ...state,
                theme: action.payload,
            };
        case 'SET_LOADING':
            return {
                ...state,
                loading: {
                    ...state.loading,
                    [action.payload.key]: action.payload.value,
                },
            };
        case 'SET_LAST_FETCH':
            return {
                ...state,
                cache: {
                    ...state.cache,
                    lastFetch: {
                        ...state.cache.lastFetch,
                        [action.payload.key]: action.payload.timestamp,
                    },
                },
            };
        case 'CLEAR_CACHE':
            return {
                ...state,
                cache: {
                    lastFetch: {},
                },
            };
        default:
            return state;
    }
}

// Context
interface GlobalContextType {
    state: GlobalState;
    dispatch: React.Dispatch<GlobalAction>;
    
    // Helper functions
    setAirlines: (airlines: any[]) => void;
    setCurrentUser: (user: any) => void;
    setTheme: (theme: 'light' | 'dark') => void;
    setLoading: (key: keyof GlobalState['loading'], value: boolean) => void;
    isCacheValid: (key: string, maxAge?: number) => boolean;
    markFetched: (key: string) => void;
}

const GlobalContext = createContext<GlobalContextType | undefined>(undefined);

// Provider component
export const GlobalStateProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [state, dispatch] = useReducer(globalReducer, initialState);

    // Helper functions
    const setAirlines = useCallback((airlines: any[]) => {
        dispatch({ type: 'SET_AIRLINES', payload: airlines });
        dispatch({ type: 'SET_LAST_FETCH', payload: { key: 'airlines', timestamp: Date.now() } });
    }, []);

    const setCurrentUser = useCallback((user: any) => {
        dispatch({ type: 'SET_CURRENT_USER', payload: user });
    }, []);

    const setTheme = useCallback((theme: 'light' | 'dark') => {
        dispatch({ type: 'SET_THEME', payload: theme });
        localStorage.setItem('theme', theme);
    }, []);

    const setLoading = useCallback((key: keyof GlobalState['loading'], value: boolean) => {
        dispatch({ type: 'SET_LOADING', payload: { key, value } });
    }, []);

    const isCacheValid = useCallback((key: string, maxAge = 5 * 60 * 1000) => {
        const lastFetch = state.cache.lastFetch[key];
        if (!lastFetch) return false;
        return Date.now() - lastFetch < maxAge;
    }, [state.cache.lastFetch]);

    const markFetched = useCallback((key: string) => {
        dispatch({ type: 'SET_LAST_FETCH', payload: { key, timestamp: Date.now() } });
    }, []);

    // Load theme from localStorage on mount
    useEffect(() => {
        const savedTheme = localStorage.getItem('theme') as 'light' | 'dark';
        if (savedTheme) {
            setTheme(savedTheme);
        }
    }, [setTheme]);

    const contextValue: GlobalContextType = {
        state,
        dispatch,
        setAirlines,
        setCurrentUser,
        setTheme,
        setLoading,
        isCacheValid,
        markFetched,
    };

    return (
        <GlobalContext.Provider value={contextValue}>
            {children}
        </GlobalContext.Provider>
    );
};

// Hook to use global state
export const useGlobalState = () => {
    const context = useContext(GlobalContext);
    if (context === undefined) {
        throw new Error('useGlobalState must be used within a GlobalStateProvider');
    }
    return context;
};
