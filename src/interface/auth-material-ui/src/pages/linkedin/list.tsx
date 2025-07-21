import React from "react";
import EditIcon from "@mui/icons-material/Edit";
import { List } from "@refinedev/mui";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import Papa, { ParseResult } from "papaparse";

type Row = {
  company_name: string;
  linkedin_url: string;
  description: string;
  fleet_size: string;
};

export const LinkedinList: React.FC = () => {
  const [rows, setRows] = React.useState<Row[]>([]);

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


  const [editRow, setEditRow] = React.useState<Row | null>(null);
  const [editIndex, setEditIndex] = React.useState<number | null>(null);

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
      {
        field: "edit",
        headerName: "Edit",
        minWidth: 80,
        sortable: false,
        filterable: false,
        renderCell: (params) => {
          // On retrouve l'index réel dans rows
          const idx = rows.findIndex(
            r => r.company_name === params.row.company_name && r.linkedin_url === params.row.linkedin_url
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

  // Filtrer les rows selon fleet_size
  const filteredRows = rows.filter(row => {
    const val = Number(row.fleet_size);
    if (isNaN(val)) return false;
    return val >= minFleetSize && val <= maxFleetSize;
  });


  return (
    <List>
      <div style={{ marginBottom: 16 }}>
        <label style={{ marginRight: 8 }}>Fleet Size min:</label>
        <input
          type="number"
          value={minFleetSize}
          min={minFleet}
          max={maxFleetSize}
          onChange={e => setMinFleetSize(Number(e.target.value))}
          style={{ width: 80, marginRight: 16 }}
        />
        <label style={{ marginRight: 8 }}>max:</label>
        <input
          type="number"
          value={maxFleetSize}
          min={minFleetSize}
          max={maxFleet}
          onChange={e => setMaxFleetSize(Number(e.target.value))}
          style={{ width: 80 }}
        />
      </div>
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
                // Envoie les données modifiées au backend pour sauvegarde dans le CSV
                try {
                  const resp = await fetch("/api/save-linkedin-csv", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ rows: updatedRows })
                  });
                  if (resp.ok) {
                    // Recharge le CSV pour afficher la version à jour
                    const res = await fetch("/linkedin_list_merged_with_fleet.csv?_=" + Date.now());
                    const csv = await res.text();
                    Papa.parse<Row>(csv, {
                      header: true,
                      skipEmptyLines: true,
                      complete: (result: ParseResult<Row>) => {
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
              <label>Company Name: </label>
              <input
                type="text"
                value={editRow.company_name}
                onChange={e => setEditRow({ ...editRow, company_name: e.target.value })}
                style={{ width: 200 }}
              />
            </div>
            <div style={{ marginBottom: 8 }}>
              <label>LinkedIn URL: </label>
              <input
                type="text"
                value={editRow.linkedin_url}
                onChange={e => setEditRow({ ...editRow, linkedin_url: e.target.value })}
                style={{ width: 200 }}
              />
            </div>
            <div style={{ marginBottom: 8 }}>
              <label>Description: </label>
              <input
                type="text"
                value={editRow.description}
                onChange={e => setEditRow({ ...editRow, description: e.target.value })}
                style={{ width: 400 }}
              />
            </div>
            <div style={{ marginBottom: 8 }}>
              <label>Fleet Size: </label>
              <input
                type="number"
                value={editRow.fleet_size}
                onChange={e => setEditRow({ ...editRow, fleet_size: e.target.value })}
                style={{ width: 100 }}
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
          rows={filteredRows.map((row, i) => ({ id: i, ...row }))}
          columns={columns}
          pagination
          paginationMode="client"
          paginationModel={paginationModel}
          onPaginationModelChange={setPaginationModel}
          pageSizeOptions={[25, 50, 100]}
          autoHeight={false}
          sx={{ minHeight: 400 }}
        />
      </div>
    </List>
  );
};
