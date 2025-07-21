
import React from "react";
import EditIcon from "@mui/icons-material/Edit";
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
  const [editRow, setEditRow] = React.useState<FleetRow | null>(null);
  const [editIndex, setEditIndex] = React.useState<number | null>(null);

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
      {
        field: "edit",
        headerName: "Edit",
        minWidth: 80,
        sortable: false,
        filterable: false,
        renderCell: (params) => {
          const idx = rows.findIndex(
            r => r.airline_name === params.row.airline_name && r.registration === params.row.registration
          );
          return (
            <button
              onClick={() => {
                setEditRow(params.row);
                setEditIndex(idx);
              }}
              style={{ background: "none", border: "none", cursor: "pointer" }}
              title="Edit"
            >
              <EditIcon />
            </button>
          );
        },
      },
    ],
    [rows]
  );

  return (
    <List>
      {editRow && (
        <div style={{ background: '#f5f5f5', padding: 16, marginBottom: 16, borderRadius: 8 }}>
          <h3>Edit Row</h3>
          <form
            onSubmit={async e => {
              e.preventDefault();
              if (editIndex !== null) {
                const updatedRows = [...rows];
                updatedRows[editIndex] = { ...editRow };
                setEditRow(null);
                setEditIndex(null);
                try {
                  const resp = await fetch("/api/save-fleet-csv", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ rows: updatedRows })
                  });
                  if (resp.ok) {
                    const res = await fetch("/fleet_data_2800.csv?_=" + Date.now());
                    const csv = await res.text();
                    Papa.parse<FleetRow>(csv, {
                      header: true,
                      skipEmptyLines: true,
                      complete: (result: ParseResult<FleetRow>) => {
                        setRows(result.data);
                      },
                    });
                    alert("Modifications enregistrées !");
                  } else {
                    alert("Erreur lors de la sauvegarde du CSV (backend)");
                  }
                } catch (err) {
                  alert("Erreur lors de la sauvegarde du CSV (réseau)");
                }
              }
            }}
          >
            <div style={{ marginBottom: 8 }}>
              <label>Airline Name: </label>
              <input
                type="text"
                value={editRow.airline_name}
                onChange={e => setEditRow({ ...editRow, airline_name: e.target.value })}
                style={{ width: 180 }}
              />
            </div>
            <div style={{ marginBottom: 8 }}>
              <label>Sigle: </label>
              <input
                type="text"
                value={editRow.sigle}
                onChange={e => setEditRow({ ...editRow, sigle: e.target.value })}
                style={{ width: 80 }}
              />
            </div>
            <div style={{ marginBottom: 8 }}>
              <label>Aircraft Type: </label>
              <input
                type="text"
                value={editRow.aircraft_type}
                onChange={e => setEditRow({ ...editRow, aircraft_type: e.target.value })}
                style={{ width: 120 }}
              />
            </div>
            <div style={{ marginBottom: 8 }}>
              <label>Registration: </label>
              <input
                type="text"
                value={editRow.registration}
                onChange={e => setEditRow({ ...editRow, registration: e.target.value })}
                style={{ width: 120 }}
              />
            </div>
            <div style={{ marginBottom: 8 }}>
              <label>Detailed Aircraft Type: </label>
              <input
                type="text"
                value={editRow.detailed_aircraft_type}
                onChange={e => setEditRow({ ...editRow, detailed_aircraft_type: e.target.value })}
                style={{ width: 180 }}
              />
            </div>
            <div style={{ marginBottom: 8 }}>
              <label>Total Fleet Size: </label>
              <input
                type="number"
                value={editRow.total_fleet_size}
                onChange={e => setEditRow({ ...editRow, total_fleet_size: e.target.value })}
                style={{ width: 80 }}
              />
            </div>
            <button type="submit" style={{ marginRight: 8 }}>Save</button>
            <button type="button" onClick={() => { setEditRow(null); setEditIndex(null); }}>Cancel</button>
          </form>
        </div>
      )}
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
