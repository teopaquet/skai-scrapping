import { useMemo } from 'react';
import { GridColDef } from '@mui/x-data-grid';
import { EditButton, ShowButton, DeleteButton } from '@refinedev/mui';

// Standard actions column that can be reused
export const useActionsColumn = (
    onEdit?: (id: string | number) => void,
    onShow?: (id: string | number) => void,
    onDelete?: (id: string | number) => void,
    minWidth = 180
): GridColDef => {
    return useMemo(() => ({
        field: "actions",
        headerName: "Actions",
        align: "right",
        headerAlign: "right",
        minWidth,
        sortable: false,
        renderCell: ({ row }) => (
            <>
                {onEdit && <EditButton hideText recordItemId={row.id} onClick={() => onEdit(row.id)} />}
                {onShow && <ShowButton hideText recordItemId={row.id} onClick={() => onShow(row.id)} />}
                {onDelete && <DeleteButton hideText recordItemId={row.id} onClick={() => onDelete(row.id)} />}
            </>
        ),
    }), [onEdit, onShow, onDelete, minWidth]);
};

// Standard ID column
export const useIdColumn = (): GridColDef => {
    return useMemo(() => ({
        field: "id",
        headerName: "ID",
        type: "number",
        minWidth: 50
    }), []);
};

// Boolean column formatter
export const useBooleanColumn = (field: string, headerName: string): GridColDef => {
    return useMemo(() => ({
        field,
        headerName,
        minWidth: 100,
        renderCell: (params) => params.value ? "Yes" : "No"
    }), [field, headerName]);
};

// Date column formatter
export const useDateColumn = (field: string, headerName: string, format: 'date' | 'datetime' = 'date'): GridColDef => {
    return useMemo(() => ({
        field,
        headerName,
        minWidth: 140,
        valueFormatter: ({ value }) => {
            if (!value) return "—";
            const date = new Date(value);
            return format === 'date' ? date.toLocaleDateString() : date.toLocaleString();
        }
    }), [field, headerName, format]);
};

// Color column with visual indicator
export const useColorColumn = (field: string = "color", headerName: string = "Color"): GridColDef => {
    return useMemo(() => ({
        field,
        headerName,
        minWidth: 120,
        renderCell: (params) => (
            <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                {params.value && (
                    <span
                        style={{
                            display: "inline-block",
                            width: 20,
                            height: 20,
                            background: params.value,
                            border: "1px solid #ccc",
                            borderRadius: 4,
                        }}
                    />
                )}
                {params.value || "—"}
            </span>
        )
    }), [field, headerName]);
};

// Text column with flex
export const useTextColumn = (field: string, headerName: string, flex = 1, minWidth = 120): GridColDef => {
    return useMemo(() => ({
        field,
        headerName,
        flex,
        minWidth,
        renderCell: (params) => params.value || "—"
    }), [field, headerName, flex, minWidth]);
};

// Email column
export const useEmailColumn = (): GridColDef => {
    return useMemo(() => ({
        field: "email",
        headerName: "Email",
        minWidth: 200,
        flex: 1,
    }), []);
};

// Custom object column (for nested data)
export const useObjectColumn = (
    field: string,
    headerName: string,
    formatter: (value: any) => string,
    minWidth = 180
): GridColDef => {
    return useMemo(() => ({
        field,
        headerName,
        minWidth,
        valueGetter: (params: any) => {
            const value = params.row[field];
            return value ? formatter(value) : "—";
        }
    }), [field, headerName, formatter, minWidth]);
};

// Specific columns for common use cases

// Base column (airport with IATA)
export const useBaseColumn = (): GridColDef => {
    return useObjectColumn("base", "Base", (base) => {
        const name = base.name || "";
        const iata = base.iata || "";
        return name && iata ? `${name} (${iata})` : name || iata || "—";
    });
};

// Aircraft column
export const useAircraftColumn = (): GridColDef => {
    return useObjectColumn("aircraft", "Aircraft", (aircraft) => {
        const registration = aircraft.registration || "";
        const name = aircraft.name || "";
        return registration && name ? `${registration} (${name})` : registration || name || "—";
    });
};

// Airport column (origin/destination)
export const useAirportColumn = (field: "origin" | "destination", headerName: string): GridColDef => {
    return useObjectColumn(field, headerName, (airport) => {
        const iata = airport.iata || "";
        const city = airport.city || airport.name || "";
        return iata && city ? `${iata} - ${city}` : iata || city || "—";
    });
};
