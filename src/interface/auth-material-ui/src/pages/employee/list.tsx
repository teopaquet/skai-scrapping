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
};

type ApiRow = {
  truncate: string;
  'invisible href': string;
  'font-qanelas': string;
  'font-qanelas 4': string;
  'inline-flex': string;
  'invisible href 2': string;
  'invisible href 3': string;
  'font-qanelas 5': string;
  'font-qanelas 6': string;
  'font-qanelas 7': string;
  'font-qanelas 8': string;
  'font-qanelas 9': string;
  'font-qanelas 10': string | number;
  'font-qanelas 11': string | number;
  'font-qanelas 12': string;
  'font-qanelas 13': string;
  'font-qanelas 14': string;
  'font-qanelas 15': string;
};

const EmployeeList: React.FC = () => {
  const [rows, setRows] = React.useState<Row[]>([]);
  const [apiRows, setApiRows] = React.useState<ApiRow[]>([]);
  // Barre de recherche
  const [search, setSearch] = React.useState("");

  React.useEffect(() => {
    // Fetch API data uniquement
    fetch("https://script.google.com/macros/s/AKfycbxrytqltihDzfDiluOdl8-5XAEIjJOb0KrmNqm2e_FcfIdftl0GNzh-WAqIbALyMdWWJQ/exec")
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) setApiRows(data);
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
          <a
            href={value}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: 'var(--mui-link-color, #1976d2)',
              textDecoration: 'underline',
              transition: 'color 0.2s',
            }}
            className="linkedin-link"
          >
            {value}
          </a>
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
        type: "number",
        sortComparator: (v1, v2) => Number(v1) - Number(v2),
      },
    ],
    []
  );

  // Colonnes dynamiques pour les données brutes
  const apiColumns = React.useMemo<GridColDef<ApiRow>[]>(() => {
    if (apiRows.length === 0) return [];
    const keys = Object.keys(apiRows[0]);
    return keys.map((key) => ({
      field: key,
      headerName: key,
      minWidth: 120,
      flex: 1,
      editable: true,
      renderCell: ({ value }) => {
        if (typeof value === 'string' && value.startsWith('http')) {
          return <a href={value} target="_blank" rel="noopener noreferrer" className="linkedin-link">{value}</a>;
        }
        return value;
      }
    }));
  }, [apiRows]);
  // Fonction pour mettre à jour une ligne dans l'API
  const handleProcessRowUpdate = async (newRow: any, oldRow: any) => {
    // L'index dans la feuille commence à 1 pour la première donnée (hors en-tête)
    // newRow.id correspond à l'index dans filteredApiRows, donc il faut retrouver l'index réel dans apiRows
    const realIndex = apiRows.findIndex(row => {
      // On compare toutes les colonnes clés pour trouver la ligne exacte
      return Object.keys(row).every(key => row[key as keyof ApiRow] === oldRow[key as keyof ApiRow]);
    });
    if (realIndex === -1) {
      alert("Impossible de trouver la ligne à modifier dans la feuille.");
      return oldRow;
    }
    const apiUrl = "https://script.google.com/macros/s/AKfycbxrytqltihDzfDiluOdl8-5XAEIjJOb0KrmNqm2e_FcfIdftl0GNzh-WAqIbALyMdWWJQ/exec?action=put";
    try {
      const { id, ...rowToSend } = newRow;
      // L'index attendu côté Apps Script commence à 1 pour la première donnée (hors en-tête)
      const body = { ...rowToSend, index: realIndex + 1 };
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const result = await response.json();
      if (!response.ok || result.status !== "success") throw new Error(result.message || "Erreur lors de la mise à jour");
      // Met à jour localement la ligne modifiée
      setApiRows((prev) => prev.map((row, i) => (i === realIndex ? { ...newRow } : row)));
      return newRow;
    } catch (error) {
      alert("Erreur lors de la mise à jour: " + error);
      return oldRow;
    }
  };

  // Pagination state
  const [paginationModel, setPaginationModel] = React.useState({ pageSize: 25, page: 0 });

  // Filtre sur le nom (search) pour les données API
  const filteredApiRows = apiRows.filter(row => {
    const name = row.truncate?.toLowerCase() || "";
    return name.includes(search.toLowerCase());
  });

  return (
    <>
      <style>{`
        .linkedin-link {
          color: var(--mui-link-color, #1976d2);
        }
        body[data-mui-color-scheme='dark'] .linkedin-link {
          color: #90caf9 !important;
        }
        .linkedin-link:hover {
          color: #1565c0;
        }
        body[data-mui-color-scheme='dark'] .linkedin-link:hover {
          color: #42a5f5 !important;
        }
      `}</style>
      <List canCreate={false}>
        <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 16 }}>
          <TextField
            label="Search Name"
            size="small"
            value={search}
            onChange={e => setSearch(e.target.value)}
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
            rows={filteredApiRows.map((row, i) => ({ id: i, ...row }))}
            columns={apiColumns}
            pagination
            pageSizeOptions={[25, 50, 100]}
            sx={{ minHeight: 400 }}
            processRowUpdate={handleProcessRowUpdate}
          />
        </div>
      </List>
    </>
  );
};

export default EmployeeList;
