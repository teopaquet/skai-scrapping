import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import React from "react";
import { List } from "@refinedev/mui";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import SearchIcon from "@mui/icons-material/Search";
import { getDatabase, ref, get } from "firebase/database";
import { firebaseApp } from "../../firebase";
import Autocomplete from "@mui/material/Autocomplete";
import Chip from "@mui/material/Chip";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";

type Row = {
  id?: number;
  company_name: string;
  linkedin_url: string;
  description: string;
  fleet_size: string;
  country?: string;
  tags?: string[];
}

export const LinkedinList: React.FC = () => {
  const [rows, setRows] = React.useState<Row[]>([]);
  // Filtres persistants
  const getInitialFilter = (key: string, fallback: any) => {
    if (typeof window === 'undefined') return fallback;
    const val = localStorage.getItem(key);
    if (val === null) return fallback;
    if (typeof fallback === 'number') return Number(val);
    return val;
  };
  // Barre de recherche
  const [search, setSearch] = React.useState(() => getInitialFilter('linkedin_search', ""));
  // Liste des tags globaux
  const [allTags, setAllTags] = React.useState<string[]>([]);
  // Pour création de tag en cours
  const [tagInput, setTagInput] = React.useState("");
  // Dialog pour gestion des tags
  const [openTagDialog, setOpenTagDialog] = React.useState(false);
  const [selectedRow, setSelectedRow] = React.useState<Row | null>(null);
  const [dialogTags, setDialogTags] = React.useState<string[]>([]);
  const [newTagName, setNewTagName] = React.useState("");

  // ...existing code...
  React.useEffect(() => {
    const db = getDatabase(firebaseApp);
    async function fetchRows() {
      const snapshot = await get(ref(db, "/Linkedin_list_with_country"));
      const data = snapshot.val();
      // Si data est un tableau ou un objet, on le transforme en tableau
      const list: Row[] = Array.isArray(data) ? data : (data ? Object.values(data) : []);
      setRows(list);
    }
    async function fetchTags() {
      const snapshot = await get(ref(db, "/tags"));
      const data = snapshot.val();
      if (Array.isArray(data)) setAllTags(data.filter(Boolean));
      else if (data && typeof data === 'object') setAllTags((Object.values(data).filter(Boolean) as string[]));
      else setAllTags([]);
    }
    fetchRows();
    fetchTags();
  }, []);



  const handleDeleteRow = async (rowId: number) => {
    // Suppression locale
    setRows(prev => prev.filter((_, i) => i !== rowId));
    // Suppression dans Firebase
    const db = getDatabase(firebaseApp);
    await import("firebase/database").then(({ ref, remove }) =>
      remove(ref(db, `/Linkedin_list_with_country/${rowId}`))
    );
    window.location.reload();
  };

  const columns = React.useMemo<GridColDef<Row>[]>(
    () => [
      {
        field: "company_name",
        headerName: "Company Name",
        minWidth: 200,
        flex: 1,
        editable: true,
      },
      {
        field: "tags",
        headerName: "Tags",
        minWidth: 200,
        flex: 1,
        editable: false,
        renderCell: (params) => {
          const tags = Array.isArray(params.value) ? params.value : [];
          return (
            <span
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '100%',
                height: '100%',
                gap: tags.length > 0 ? 8 : 0,
              }}
            >
              {tags.length > 0 && (
                <span
                  style={{ display: 'flex', gap: 6, flexWrap: 'wrap', cursor: 'pointer', userSelect: 'none' }}
                  onClick={e => {
                    e.stopPropagation();
                    setSelectedRow(params.row);
                    setDialogTags(tags);
                    setOpenTagDialog(true);
                  }}
                  title="Gérer les tags"
                >
                  {tags.map((tag, idx) => (
                    <Chip
                      key={tag + idx}
                      label={tag}
                      color="primary"
                      size="small"
                      style={{ borderRadius: 16, fontWeight: 500, background: '#1976d2', color: '#fff' }}
                    />
                  ))}
                </span>
              )}
              <span style={{ display: 'flex', alignItems: 'center' }}>
                <Button
                  size="small"
                  variant="text"
                  style={{ lineHeight: 1, fontSize: 18, alignSelf: 'center', margin: 0, padding: 0, minWidth: 0 }}
                  onClick={e => {
                    e.stopPropagation();
                    setSelectedRow(params.row);
                    setDialogTags(tags);
                    setOpenTagDialog(true);
                  }}
                  title="Ajouter ou modifier les tags"
                >
                  <AddIcon fontSize="small" style={{ color: '#555', position: 'relative' }} />
                </Button>
              </span>
            </span>
          );
        },
      },
      {
        field: "fleet_size",
        headerName: "Fleet Size",
        minWidth: 100,
        flex: 0.3,
        type: "number",
        editable: true,
        sortComparator: (v1, v2) => Number(v1) - Number(v2),
        align: 'center',
        headerAlign: 'center',
      },
      {
        field: "linkedin_url",
        headerName: "LinkedIn",
        minWidth: 200,
        flex: 1,
        editable: true,
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
        field: "country",
        headerName: "Country",
        minWidth: 120,
        flex: 0.5,
        editable: true,
      },
      {
        field: "description",
        headerName: "Description",
        minWidth: 400,
        flex: 2,
        editable: true,
      },
      {
        field: "actions",
        headerName: "",
        minWidth: 40,
        width: 40,
        flex: 0,
        sortable: false,
        filterable: false,
        disableColumnMenu: true,
        renderCell: (params) => (
          <Button
            color="error"
            size="small"
            onClick={e => {
              e.stopPropagation();
              if (window.confirm("Supprimer cette compagnie ?")) {
                const rowId = params.row.id;
                if (typeof rowId === 'number') {
                  handleDeleteRow(rowId);
                }
              }
            }}
            title="Supprimer la compagnie"
            style={{ minWidth: 0, padding: 4 }}
          >
            <DeleteIcon fontSize="small" />
          </Button>
        ),
      },
    ],
    []
  );



  // Pagination state
  const [paginationModel, setPaginationModel] = React.useState({ pageSize: 25, page: 0 });

  // Filtre min/max fleet_size
  const fleetSizes = rows.map(r => Number(r.fleet_size)).filter(n => !isNaN(n));
  const minFleet = fleetSizes.length ? Math.min(...fleetSizes) : 1;
  const maxFleet = fleetSizes.length ? Math.max(...fleetSizes) : 1000;
  const [minFleetSize, setMinFleetSize] = React.useState(() => getInitialFilter('linkedin_minFleetSize', minFleet));
  const [maxFleetSize, setMaxFleetSize] = React.useState(() => getInitialFilter('linkedin_maxFleetSize', maxFleet));

  // Persistance des filtres dans localStorage
  React.useEffect(() => {
    if (typeof window === 'undefined') return;
    localStorage.setItem('linkedin_search', search);
  }, [search]);
  React.useEffect(() => {
    if (typeof window === 'undefined') return;
    localStorage.setItem('linkedin_minFleetSize', String(minFleetSize));
  }, [minFleetSize]);
  React.useEffect(() => {
    if (typeof window === 'undefined') return;
    localStorage.setItem('linkedin_maxFleetSize', String(maxFleetSize));
  }, [maxFleetSize]);

  // Filtrer les rows selon fleet_size et recherche
  // Ajoute l'index réel à chaque row pour DataGrid
  const filteredRows = rows
    .map((row, i) => ({ ...row, id: i }))
    .filter(row => {
      const val = Number(row.fleet_size);
      if (isNaN(val)) return false;
      const matchesSearch = row.company_name.toLowerCase().includes(search.toLowerCase());
      return val >= minFleetSize && val <= maxFleetSize && matchesSearch;
    });

  // État pour la création
  const [openCreateDialog, setOpenCreateDialog] = React.useState(false);
  const [newCompany, setNewCompany] = React.useState<Row>({
    company_name: '',
    linkedin_url: '',
    description: '',
    fleet_size: '',
    country: '',
    tags: [],
  });

  // Fonction pour créer une nouvelle compagnie
  const handleCreateCompany = async () => {
    // Ajout local
    setRows(prev => [...prev, { ...newCompany }]);
    // Ajout Firebase
    const db = getDatabase(firebaseApp);
    const newId = rows.length;
    await import("firebase/database").then(({ ref, set }) =>
      set(ref(db, `/Linkedin_list_with_country/${newId}`), { ...newCompany })
    );
    setOpenCreateDialog(false);
    setNewCompany({ company_name: '', linkedin_url: '', description: '', fleet_size: '', country: '', tags: [] });
    window.location.reload();
  };

  // Calcul de la somme des fleet_size filtrés
  const totalFleetSize = filteredRows.reduce((sum, row) => {
    const val = Number(row.fleet_size);
    return !isNaN(val) ? sum + val : sum;
  }, 0);


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
        {/* Dialog de création d'une nouvelle airline */}
        <Dialog open={openCreateDialog} onClose={() => setOpenCreateDialog(false)}>
          <DialogTitle>Créer une nouvelle compagnie</DialogTitle>
          <DialogContent>
            <TextField
              label="Nom de la compagnie"
              value={newCompany.company_name}
              onChange={e => setNewCompany(c => ({ ...c, company_name: e.target.value }))}
              fullWidth
              margin="dense"
            />
            <TextField
              label="LinkedIn URL"
              value={newCompany.linkedin_url}
              onChange={e => setNewCompany(c => ({ ...c, linkedin_url: e.target.value }))}
              fullWidth
              margin="dense"
            />
            <TextField
              label="Description"
              value={newCompany.description}
              onChange={e => setNewCompany(c => ({ ...c, description: e.target.value }))}
              fullWidth
              margin="dense"
            />
            <TextField
              label="Fleet Size"
              value={newCompany.fleet_size}
              onChange={e => setNewCompany(c => ({ ...c, fleet_size: e.target.value }))}
              type="number"
              fullWidth
              margin="dense"
            />
            <TextField
              label="Country"
              value={newCompany.country}
              onChange={e => setNewCompany(c => ({ ...c, country: e.target.value }))}
              fullWidth
              margin="dense"
            />
            <Autocomplete
              multiple
              options={allTags}
              value={newCompany.tags}
              onChange={(_, newValue) => setNewCompany(c => ({ ...c, tags: newValue }))}
              renderTags={(tagValue, getTagProps) =>
                tagValue.map((option, index) => (
                  <Chip variant="outlined" label={option} {...getTagProps({ index })} key={option} />
                ))
              }
              renderInput={paramsInput => (
                <TextField {...paramsInput} variant="standard" label="Tags" />
              )}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenCreateDialog(false)}>Annuler</Button>
            <Button variant="contained" onClick={handleCreateCompany}>Créer</Button>
          </DialogActions>
        </Dialog>
        <div style={{ fontWeight: 500, fontSize: 16, color: '#1976d2', marginBottom: 12 }}>
          Total fleet size: {totalFleetSize}
        </div>

        <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 16 }}>
          <TextField
            label="Search airline"
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
            label="Min fleet size"
            type="number"
            size="small"
            value={minFleetSize}
            onChange={e => setMinFleetSize(Number(e.target.value))}
            style={{ marginRight: 16 }}
          />
          <TextField
            label="Max fleet size"
            type="number"
            size="small"
            value={maxFleetSize}
            onChange={e => setMaxFleetSize(Number(e.target.value))}
          />
          <div style={{ flex: 1 }} />
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={() => setOpenCreateDialog(true)}
            style={{ marginLeft: 'auto', whiteSpace: 'nowrap' }}
          >
            Add a company
          </Button>
        </div>
        <Dialog open={openTagDialog} onClose={() => setOpenTagDialog(false)}>
          <DialogTitle>Manage tags for {selectedRow?.company_name}</DialogTitle>
          <DialogContent>
            <div style={{ marginBottom: 12 }}>
              <Autocomplete
                multiple
                options={allTags}
                value={dialogTags}
                onChange={(_, newValue) => setDialogTags(newValue)}
                renderTags={(tagValue, getTagProps) =>
                  tagValue.map((option, index) => (
                    <Chip variant="outlined" label={option} {...getTagProps({ index })} key={option} />
                  ))
                }
                renderInput={paramsInput => (
                  <TextField {...paramsInput} variant="standard" label="Tags to assign" />
                )}
              />
            </div>
            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              <TextField
                label="New tag"
                size="small"
                value={newTagName}
                onChange={e => setNewTagName(e.target.value)}
                onKeyDown={e => {
                  if (e.key === 'Enter' && newTagName.trim()) {
                    if (!allTags.includes(newTagName.trim())) {
                      const newTags = [...allTags, newTagName.trim()];
                      setAllTags(newTags);
                      setDialogTags(prev => [...prev, newTagName.trim()]);
                      // Save to Firebase
                      const db = getDatabase(firebaseApp);
                      import("firebase/database").then(({ ref, set }) =>
                        set(ref(db, "/tags"), newTags)
                      );
                    } else if (!dialogTags.includes(newTagName.trim())) {
                      setDialogTags(prev => [...prev, newTagName.trim()]);
                    }
                    setNewTagName("");
                  }
                }}
              />
              <Button onClick={() => {
                if (newTagName.trim()) {
                  if (!allTags.includes(newTagName.trim())) {
                    const newTags = [...allTags, newTagName.trim()];
                    setAllTags(newTags);
                    setDialogTags(prev => [...prev, newTagName.trim()]);
                    // Save to Firebase
                    const db = getDatabase(firebaseApp);
                    import("firebase/database").then(({ ref, set }) =>
                      set(ref(db, "/tags"), newTags)
                    );
                  } else if (!dialogTags.includes(newTagName.trim())) {
                    setDialogTags(prev => [...prev, newTagName.trim()]);
                  }
                  setNewTagName("");
                }
              }} variant="contained" size="small">Add</Button>
            </div>
            <div style={{ marginTop: 16, fontSize: 13, color: '#888' }}>
              <b>Existing tags:</b> {allTags.join(', ')}
            </div>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenTagDialog(false)}>Cancel</Button>
            <Button variant="contained" onClick={async () => {
              if (!selectedRow) return;
              // Met à jour localement
              setRows(prev => prev.map(r => r === selectedRow ? { ...r, tags: dialogTags } : r));
              // Met à jour dans Firebase
              const db = getDatabase(firebaseApp);
              const { id, ...rowToSave } = { ...selectedRow, tags: dialogTags };
              await import("firebase/database").then(({ ref, set }) =>
                set(ref(db, `/Linkedin_list_with_country/${selectedRow.id}`), { ...rowToSave })
              );
              setOpenTagDialog(false);
              window.location.reload();
            }}>Save</Button>
          </DialogActions>
        </Dialog>
        {/* Filtres déplacés ci-dessus */}

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            maxHeight: "calc(100vh - 320px)",
          }}
        >
          <DataGrid
            rows={filteredRows}
            columns={columns}
            pagination
            paginationMode="client"
            paginationModel={paginationModel}
            onPaginationModelChange={setPaginationModel}
            pageSizeOptions={[25, 50, 100]}
            sx={{ minHeight: 400 }}
            getRowHeight={() => 'auto'}
            processRowUpdate={async (newRow, oldRow) => {
              // Update locally
              setRows(prev => prev.map((r, i) => i === newRow.id ? { ...newRow } : r));
              // Update in Firebase
              const db = getDatabase(firebaseApp);
              const { id, ...rowToSave } = newRow;
              await import("firebase/database").then(({ ref, set }) =>
                set(ref(db, `/Linkedin_list_with_country/${newRow.id}`), { ...rowToSave })
              );
              return newRow;
            }}
            onProcessRowUpdateError={error => {
              // Log error in console
              console.error('Error while saving to Firebase:', error);
            }}
          />
        </div>
      </List>
    </>
  );
}
