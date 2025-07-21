import React, { Suspense, lazy } from 'react';
import { CircularProgress, Box } from '@mui/material';

// Loading component
const LoadingSpinner = () => (
    <Box 
        display="flex" 
        justifyContent="center" 
        alignItems="center" 
        minHeight="200px"
    >
        <CircularProgress />
    </Box>
);

// Higher-order component for lazy loading
// export const withLazyLoading = <P extends object>(
//     importFunc: () => Promise<{ default: React.ComponentType<P> }>,
//     FallbackComponent?: React.ComponentType
// ) => {
//     const LazyComponent = lazy(importFunc);
    
//     const WrappedComponent: React.FC<P> = (props) => (
//         <Suspense fallback={FallbackComponent ? <FallbackComponent /> : <LoadingSpinner />}>
//             <LazyComponent {...props} />
//         </Suspense>
//     );
//     return WrappedComponent;
// };

