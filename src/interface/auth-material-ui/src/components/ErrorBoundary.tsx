import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Box, Typography, Button, Paper, Alert } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

interface Props {
    children: ReactNode;
    fallback?: ReactNode;
}

interface State {
    hasError: boolean;
    error?: Error;
    errorInfo?: ErrorInfo;
}

export class ErrorBoundary extends Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('ErrorBoundary caught an error:', error, errorInfo);
        this.setState({ error, errorInfo });
        
        // Log to external service in production
        if (process.env.NODE_ENV === 'production') {
            // Send to error tracking service
            console.error('Production error:', { error, errorInfo });
        }
    }

    handleReset = () => {
        this.setState({ hasError: false, error: undefined, errorInfo: undefined });
    };

    render() {
        if (this.state.hasError) {
            if (this.props.fallback) {
                return this.props.fallback;
            }

            return (
                <Box
                    display="flex"
                    flexDirection="column"
                    alignItems="center"
                    justifyContent="center"
                    minHeight="400px"
                    p={3}
                >
                    <Paper
                        elevation={3}
                        sx={{
                            p: 4,
                            maxWidth: 600,
                            textAlign: 'center',
                        }}
                    >
                        <Alert severity="error" sx={{ mb: 3 }}>
                            <Typography variant="h6" gutterBottom>
                                Something went wrong
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                                {this.state.error?.message || 'An unexpected error occurred'}
                            </Typography>
                        </Alert>

                        <Button
                            variant="contained"
                            startIcon={<RefreshIcon />}
                            onClick={this.handleReset}
                            sx={{ mr: 2 }}
                        >
                            Try Again
                        </Button>
                        
                        <Button
                            variant="outlined"
                            onClick={() => window.location.reload()}
                        >
                            Reload Page
                        </Button>

                        {process.env.NODE_ENV === 'development' && (
                            <Box mt={3} textAlign="left">
                                <Typography variant="subtitle2" gutterBottom>
                                    Error Details (Development):
                                </Typography>
                                <pre
                                    style={{
                                        background: '#f5f5f5',
                                        padding: '16px',
                                        borderRadius: '4px',
                                        overflow: 'auto',
                                        fontSize: '12px',
                                        maxHeight: '200px',
                                    }}
                                >
                                    {this.state.error?.stack}
                                </pre>
                            </Box>
                        )}
                    </Paper>
                </Box>
            );
        }

        return this.props.children;
    }
}

// Hook for error handling in functional components
export const useErrorHandler = () => {
    const [error, setError] = React.useState<Error | null>(null);

    const resetError = React.useCallback(() => {
        setError(null);
    }, []);

    const handleError = React.useCallback((error: Error) => {
        console.error('Error caught by hook:', error);
        setError(error);
    }, []);

    // Throw error to trigger error boundary
    if (error) {
        throw error;
    }

    return { handleError, resetError };
};
