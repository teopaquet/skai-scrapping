import React from "react";
import { List } from "@refinedev/mui";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import SearchIcon from "@mui/icons-material/Search";
import Papa, { ParseResult } from "papaparse";

type Row = {
  company_name: string;
  linkedin_url: string;
  description: string;
  fleet_size: string;
}

export const LinkedinList: React.FC = () => {
  const [rows, setRows] = React.useState<Row[]>([]);
  // Barre de recherche
  const [search, setSearch] = React.useState("");

  React.useEffect(() => {
    fetch("/linkedin_list_merged_with_fleet.csv")
      .then((res) => res.text())
      .then((csv) => {
        Papa.parse<Row>(csv, {
          header: true,
          skipEmptyLines: true,
          complete: (result: ParseResult<Row>) => {
            setRows(result.data);
          },
        });
      });
  }, []);



  const columns = React.useMemo<GridColDef<Row>[]>(
    () => [
      {
        field: "company_name",
        headerName: "Company Name",
        minWidth: 200,
        flex: 1,
      },
      {
        field: "linkedin_url",
        headerName: "LinkedIn",
        minWidth: 200,
        flex: 1,
        renderCell: ({ value }) => (
          <a href={value} target="_blank" rel="noopener noreferrer">{value}</a>
        ),
      },
      {
        field: "description",
        headerName: "Description",
        minWidth: 400,
        flex: 2,
      },
      {
        field: "fleet_size",
        headerName: "Fleet Size",
        minWidth: 100,
        flex: 0.3,
      },
    ],
    []
  );



  // Pagination state
  const [paginationModel, setPaginationModel] = React.useState({ pageSize: 25, page: 0 });

  // Filtre min/max fleet_size
  const fleetSizes = rows.map(r => Number(r.fleet_size)).filter(n => !isNaN(n));
  const minFleet = fleetSizes.length ? Math.min(...fleetSizes) : 0;
  const maxFleet = fleetSizes.length ? Math.max(...fleetSizes) : 100;
  const [minFleetSize, setMinFleetSize] = React.useState(minFleet);
  const [maxFleetSize, setMaxFleetSize] = React.useState(maxFleet);

  // Filtrer les rows selon fleet_size et recherche
  const filteredRows = rows.filter(row => {
    const val = Number(row.fleet_size);
    if (isNaN(val)) return false;
    const matchesSearch = row.company_name.toLowerCase().includes(search.toLowerCase());
    return val >= minFleetSize && val <= maxFleetSize && matchesSearch;
  });


  return (
    <List canCreate={false}>
      <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 16 }}>
        <TextField
          label="Rechercher une compagnie"
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
}
