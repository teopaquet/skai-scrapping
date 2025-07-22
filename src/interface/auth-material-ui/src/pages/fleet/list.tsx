
import React from "react";
import { List } from "@refinedev/mui";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import Papa, { ParseResult } from "papaparse";

type FleetRow = {
  airline_name: string;
  sigle: string;
  aircraft_type: string;
  registration: string;
  detailed_aircraft_type: string;
  total_fleet_size: string;
};

export const FleetList: React.FC = () => {
  const [rows, setRows] = React.useState<FleetRow[]>([]);

  React.useEffect(() => {
    fetch("/fleet_data_2800.csv")
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
      { field: "total_fleet_size", headerName: "Total Fleet Size", minWidth: 80, flex: 0.5 },
    ],
    []
  );

  return (
    <List canCreate={false}>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          maxHeight: "calc(100vh - 320px)",
        }}
      >
        <DataGrid
          rows={rows.map((row, i) => ({ id: i, ...row }))}
          columns={columns}
          pagination
          pageSizeOptions={[25, 50, 100]}
          autoHeight={false}
          sx={{ minHeight: 400 }}
        />
      </div>
    </List>
  );
};
