
import React from "react";
import { List } from "@refinedev/mui";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import SearchIcon from "@mui/icons-material/Search";
import Papa, { ParseResult } from "papaparse";

type FleetRow = {
  airline_name: string;
  sigle: string;
  aircraft_type: string;
  registration: string;
  detailed_aircraft_type: string;
  total_fleet_size: string;
  country?: string;
};

export const FleetList: React.FC = () => {
  const [rows, setRows] = React.useState<FleetRow[]>([]);
  // Barre de recherche
  const [search, setSearch] = React.useState("");

  React.useEffect(() => {
    fetch("/fleet_data_2800_with_country.csv")
      .then((res) => res.text())
      .then((csv) => {
        Papa.parse<FleetRow>(csv, {
          header: true,
          skipEmptyLines: true,
          complete: (result: ParseResult<FleetRow>) => {
            setRows(result.data);
          },
        });
      });
  }, []);

  const columns = React.useMemo<GridColDef<FleetRow>[]>(
    () => [
      { field: "airline_name", headerName: "Airline Name", minWidth: 180, flex: 1 },
      { field: "sigle", headerName: "Sigle", minWidth: 80, flex: 0.5 },
      { field: "aircraft_type", headerName: "Aircraft Type", minWidth: 120, flex: 1 },
      { field: "registration", headerName: "Registration", minWidth: 120, flex: 1 },
      { field: "detailed_aircraft_type", headerName: "Detailed Type", minWidth: 180, flex: 1 },
      { field: "country", headerName: "Country", minWidth: 120, flex: 1 },
      {
        field: "total_fleet_size",
        headerName: "Total Fleet Size",
        minWidth: 80,
        flex: 0.5,
        type: "number",
        sortComparator: (v1, v2) => Number(v1) - Number(v2),
      },
    ],
    []
  );

  // Filtre min/max total_fleet_size
  const fleetSizes = rows.map(r => Number(r.total_fleet_size)).filter(n => !isNaN(n));
  const minFleet = fleetSizes.length ? Math.min(...fleetSizes) : 1;
  const maxFleet = fleetSizes.length ? Math.max(...fleetSizes) : 1000;
  const [minFleetSize, setMinFleetSize] = React.useState(minFleet);
  const [maxFleetSize, setMaxFleetSize] = React.useState(maxFleet);

  // Filtrer les rows selon total_fleet_size et recherche
  const filteredRows = rows.filter(row => {
    const val = Number(row.total_fleet_size);
    if (isNaN(val)) return false;
    const matchesSearch = row.airline_name.toLowerCase().includes(search.toLowerCase());
    return val >= minFleetSize && val <= maxFleetSize && matchesSearch;
  });

  // Pagination state
  const [paginationModel, setPaginationModel] = React.useState({ pageSize: 25, page: 0 });

  return (
    <List canCreate={false}>
      <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 16 }}>
        <TextField
          label="Search Airline"
          size="small"
          value={search}
          onChange={e => setSearch(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
            style: { width: 260 }
          }}
          style={{ marginRight: 16 }}
        />
        <TextField
          label="Fleet Size min"
          type="number"
          size="small"
          value={minFleetSize}
          onChange={e => setMinFleetSize(Number(e.target.value))}
          style={{ marginRight: 16 }}
        />
        <TextField
          label="max"
          type="number"
          size="small"
          value={maxFleetSize}
          onChange={e => setMaxFleetSize(Number(e.target.value))}
        />
      </div>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          maxHeight: "calc(100vh - 320px)",
        }}
      >
        <DataGrid
          rows={filteredRows.map((row, i) => ({ id: i, ...row }))}
          columns={columns}
          pagination
          paginationMode="client"
          paginationModel={paginationModel}
          onPaginationModelChange={setPaginationModel}
          pageSizeOptions={[25, 50, 100]}
          sx={{ minHeight: 400 }}
        />
      </div>
    </List>
  );
};
