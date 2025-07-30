import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import React from "react";
import Snackbar from "@mui/material/Snackbar";
import MuiAlert, { AlertProps } from "@mui/material/Alert";
import Skeleton from "@mui/material/Skeleton";
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
  const [loading, setLoading] = React.useState(true);
  const [snackbar, setSnackbar] = React.useState<{open: boolean, message: string, severity: 'success'|'error'|'info'|'warning'}>({open: false, message: '', severity: 'success'});
// Persistent filters
  const getInitialFilter = (key: string, fallback: any) => {
    if (typeof window === 'undefined') return fallback;
    const val = localStorage.getItem(key);
    if (val === null) return fallback;
    if (typeof fallback === 'number') return Number(val);
    return val;
  };
  // Search bar
  const [search, setSearch] = React.useState(() => getInitialFilter('linkedin_search', ""));
  // List of global tags
  const [allTags, setAllTags] = React.useState<string[]>([]);
  // For tag creation in progress
  const [tagInput, setTagInput] = React.useState("");
  // Dialog for tag management
  const [openTagDialog, setOpenTagDialog] = React.useState(false);
  const [selectedRow, setSelectedRow] = React.useState<Row | null>(null);
  const [dialogTags, setDialogTags] = React.useState<string[]>([]);
  const [newTagName, setNewTagName] = React.useState("");

  // For delete confirmation
  const [deleteDialogOpen, setDeleteDialogOpen] = React.useState(false);
  const [rowToDelete, setRowToDelete] = React.useState<Row | null>(null);

  // Add state for tag delete confirmation
  const [openDeleteTagDialog, setOpenDeleteTagDialog] = React.useState(false);
  const [tagToDelete, setTagToDelete] = React.useState<string | null>(null);

  React.useEffect(() => {
    const db = getDatabase(firebaseApp);
    async function fetchRows() {
      try {
        const snapshot = await get(ref(db, "/Linkedin_list_with_country"));
        const data = snapshot.val();
        const list: Row[] = Array.isArray(data) ? data : (data ? Object.values(data) : []);
        setRows(list);
      } catch (e) {
        setSnackbar({open: true, message: 'Error loading companies', severity: 'error'});
      } finally {
        setLoading(false);
      }
    }
    async function fetchTags() {
      try {
        const snapshot = await get(ref(db, "/tags"));
        const data = snapshot.val();
        if (Array.isArray(data)) setAllTags(data.filter(Boolean));
        else if (data && typeof data === 'object') setAllTags((Object.values(data).filter(Boolean) as string[]));
        else setAllTags([]);
      } catch (e) {
        setSnackbar({open: true, message: 'Error loading tags', severity: 'error'});
      }
    }
    fetchRows();
    fetchTags();
  }, []);



  const handleDeleteRow = async (rowId: number) => {
    try {
      setRows(prev => prev.filter((_, i) => i !== rowId));
      const db = getDatabase(firebaseApp);
      await import("firebase/database").then(({ ref, remove }) =>
        remove(ref(db, `/Linkedin_list_with_country/${rowId}`))
      );
      setSnackbar({open: true, message: 'Company deleted', severity: 'success'});
      setTimeout(() => window.scrollTo({top: 0, behavior: 'smooth'}), 200);
      setTimeout(() => window.location.reload(), 800);
    } catch (e) {
      setSnackbar({open: true, message: 'Error while deleting', severity: 'error'});
    }
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
                justifyContent: 'flex-start',
                width: '100%',
                height: '100%',
                gap: tags.length > 0 ? 8 : 0,
              }}
            >
              {tags.length > 0 ? (
                <span
                  style={{ display: 'flex', gap: 6, flexWrap: 'wrap', cursor: 'pointer', userSelect: 'none', alignItems: 'center' }}
                  onClick={e => {
                    e.stopPropagation();
                    setSelectedRow(params.row);
                    setDialogTags(tags);
                    setOpenTagDialog(true);
                  }}
                  title="Manage tags"
                >
                  {tags.map((tag, idx) => (
                    <Chip
                      key={tag + idx}
                      label={tag}
                      size="small"
                      style={{
                        borderRadius: 16,
                        fontWeight: 500,
                        background: getTagColor(tag),
                        color: '#fff',
                        letterSpacing: 0.2,
                        boxShadow: '0 1px 4px #0001',
                        fontSize: 13,
                        marginRight: idx === tags.length - 1 ? 0 : 0,
                      }}
                    />
                  ))}
                </span>
              ) : (
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
                  title="Add or edit tags"
                >
                  <AddIcon fontSize="small" style={{ color: '#555', position: 'relative' }} />
                </Button>
              )}
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
              setRowToDelete(params.row);
              setDeleteDialogOpen(true);
            }}
            title="Delete company"
            style={{ minWidth: 0, padding: 4 }}
          >
            <DeleteIcon fontSize="small" />
          </Button>
        ),
      },
    ],
    []
  );



  // Pagination state with persistence
  const getInitialPagination = () => {
    if (typeof window === 'undefined') return { pageSize: 25, page: 0 };
    const saved = localStorage.getItem('linkedin_pagination');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (
          typeof parsed === 'object' &&
          typeof parsed.page === 'number' &&
          typeof parsed.pageSize === 'number'
        ) {
          return parsed;
        }
      } catch {}
    }
    return { pageSize: 25, page: 0 };
  };
  const [paginationModel, setPaginationModel] = React.useState(getInitialPagination);

  // Persist pagination in localStorage
  React.useEffect(() => {
    if (typeof window === 'undefined') return;
    localStorage.setItem('linkedin_pagination', JSON.stringify(paginationModel));
  }, [paginationModel]);

  // Min/max fleet_size filter
  const fleetSizes = rows.map(r => Number(r.fleet_size)).filter(n => !isNaN(n));
  const minFleet = fleetSizes.length ? Math.min(...fleetSizes) : 1;
  const maxFleet = fleetSizes.length ? Math.max(...fleetSizes) : 1000;
  const [minFleetSize, setMinFleetSize] = React.useState(() => getInitialFilter('linkedin_minFleetSize', minFleet));
  const [maxFleetSize, setMaxFleetSize] = React.useState(() => getInitialFilter('linkedin_maxFleetSize', maxFleet));

  // Persist filters in localStorage
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

  // Filter rows by fleet_size and search
  // Add real index to each row for DataGrid
  const filteredRows = rows
    .map((row, i) => ({ ...row, id: i }))
    .filter(row => {
      const val = Number(row.fleet_size);
      if (isNaN(val)) return false;
      const matchesSearch = row.company_name.toLowerCase().includes(search.toLowerCase());
      return val >= minFleetSize && val <= maxFleetSize && matchesSearch;
    });

  // State for creation
  const [openCreateDialog, setOpenCreateDialog] = React.useState(false);
  const [newCompany, setNewCompany] = React.useState<Row>({
    company_name: '',
    linkedin_url: '',
    description: '',
    fleet_size: '',
    country: '',
    tags: [],
  });
  const firstInputRef = React.useRef<HTMLInputElement>(null);
  React.useEffect(() => {
    if (openCreateDialog && firstInputRef.current) {
      setTimeout(() => firstInputRef.current?.focus(), 200);
    }
  }, [openCreateDialog]);

  // Function to create a new company
  const handleCreateCompany = async () => {
    // Validation
    if (!newCompany.company_name.trim() || !newCompany.fleet_size.trim() || isNaN(Number(newCompany.fleet_size))) {
      setSnackbar({open: true, message: 'Name and fleet size required', severity: 'warning'});
      return;
    }
    try {
      setRows(prev => [...prev, { ...newCompany }]);
      const db = getDatabase(firebaseApp);
      const newId = rows.length;
      await import("firebase/database").then(({ ref, set }) =>
        set(ref(db, `/Linkedin_list_with_country/${newId}`), { ...newCompany })
      );
      setOpenCreateDialog(false);
      setNewCompany({ company_name: '', linkedin_url: '', description: '', fleet_size: '', country: '', tags: [] });
      setSnackbar({open: true, message: 'Company created', severity: 'success'});
      setTimeout(() => window.scrollTo({top: 0, behavior: 'smooth'}), 200);
      setTimeout(() => window.location.reload(), 800);
    } catch (e) {
      setSnackbar({open: true, message: 'Error while creating', severity: 'error'});
    }
  };

  // Calculate the sum of filtered fleet_size
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
        .MuiDataGrid-row:hover {
          background: #f5faff !important;
        }
        .MuiButton-containedPrimary {
          transition: background 0.2s;
        }
        .MuiButton-containedPrimary:active {
          background: #115293;
        }
        .MuiDialog-root .MuiPaper-root {
          transition: box-shadow 0.3s cubic-bezier(.4,0,.2,1);
        }
      `}</style>
      <List canCreate={false}>
        {/* Snackbar for user feedback */}
        <Snackbar
          open={snackbar.open}
          autoHideDuration={2500}
          onClose={() => setSnackbar(s => ({...s, open: false}))}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        >
          <MuiAlert elevation={6} variant="filled" severity={snackbar.severity} sx={{ minWidth: 220 }}>
            {snackbar.message}
          </MuiAlert>
        </Snackbar>
        {/* Dialog to create a new airline with transition and focus */}
        <Dialog open={openCreateDialog} onClose={() => setOpenCreateDialog(false)} TransitionProps={{ appear: true }}>
          <DialogTitle>Create a new company</DialogTitle>
          <DialogContent>
            <TextField
              label="Company name"
              value={newCompany.company_name}
              onChange={e => setNewCompany(c => ({ ...c, company_name: e.target.value }))}
              fullWidth
              margin="dense"
              inputRef={firstInputRef}
              required
              autoFocus
            />
            <TextField
              label="LinkedIn URL"
              value={newCompany.linkedin_url}
              onChange={e => setNewCompany(c => ({ ...c, linkedin_url: e.target.value }))}
              fullWidth
              margin="dense"
              placeholder="https://linkedin.com/company/..."
            />
            <TextField
              label="Description"
              value={newCompany.description}
              onChange={e => setNewCompany(c => ({ ...c, description: e.target.value }))}
              fullWidth
              margin="dense"
              multiline
              minRows={2}
            />
            <TextField
              label="Fleet Size"
              value={newCompany.fleet_size}
              onChange={e => setNewCompany(c => ({ ...c, fleet_size: e.target.value }))}
              type="number"
              fullWidth
              margin="dense"
              required
              inputProps={{ min: 1 }}
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
            <Button onClick={() => setOpenCreateDialog(false)}>Cancel</Button>
            <Button variant="contained" onClick={handleCreateCompany} color="primary">Create</Button>
          </DialogActions>
        </Dialog>
        <div style={{ fontWeight: 500, fontSize: 16, color: '#1976d2', marginBottom: 12, marginTop: 8 }}>
          Total fleet size: {totalFleetSize}
        </div>
        <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
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
              style: { width: 260 },
              placeholder: '...'
            }}
            style={{ marginRight: 16, minWidth: 220 }}
          />
          <TextField
            label="Min fleet size"
            type="number"
            size="small"
            value={minFleetSize}
            onChange={e => setMinFleetSize(Number(e.target.value))}
            style={{ marginRight: 16, minWidth: 120 }}
            inputProps={{ min: 1 }}
          />
          <TextField
            label="Max fleet size"
            type="number"
            size="small"
            value={maxFleetSize}
            onChange={e => setMaxFleetSize(Number(e.target.value))}
            style={{ minWidth: 120 }}
            inputProps={{ min: 1 }}
          />
          <div style={{ flex: 1 }} />
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={() => setOpenCreateDialog(true)}
            style={{ marginLeft: 'auto', whiteSpace: 'nowrap', fontWeight: 600, fontSize: 15, boxShadow: '0 2px 8px #1976d220' }}
          >
            Add a company
          </Button>
        </div>
        <Dialog open={openTagDialog} onClose={() => setOpenTagDialog(false)} TransitionProps={{ appear: true }}>
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
                placeholder="Add a tag..."
              />
              <Button onClick={() => {
                if (newTagName.trim()) {
                  if (!allTags.includes(newTagName.trim())) {
                    const newTags = [...allTags, newTagName.trim()];
                    setAllTags(newTags);
                    setDialogTags(prev => [...prev, newTagName.trim()]);
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
              <b>Existing tags:</b>
              <span style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 6 }}>
                {allTags.map((tag, idx) => (
                  <Chip
                    key={tag + idx}
                    label={tag}
                    size="small"
                    style={{ borderRadius: 16, fontWeight: 500, background: '#e3e3e3', color: '#333' }}
                    onDelete={() => {
                      setTagToDelete(tag);
                      setOpenDeleteTagDialog(true);
                    }}
                  />
                ))}
              </span>
            </div>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenTagDialog(false)}>Cancel</Button>
            <Button variant="contained" onClick={async () => {
              if (!selectedRow) return;
              setRows(prev => prev.map(r => r === selectedRow ? { ...r, tags: dialogTags } : r));
              const db = getDatabase(firebaseApp);
              const { id, ...rowToSave } = { ...selectedRow, tags: dialogTags };
              await import("firebase/database").then(({ ref, set }) =>
                set(ref(db, `/Linkedin_list_with_country/${selectedRow.id}`), { ...rowToSave })
              );
              setOpenTagDialog(false);
              setSnackbar({open: true, message: 'Tags updated', severity: 'success'});
              setTimeout(() => window.scrollTo({top: 0, behavior: 'smooth'}), 200);
              setTimeout(() => window.location.reload(), 800);
            }}>Save</Button>
          </DialogActions>
        </Dialog>
        {/* Delete confirmation dialog */}
        <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
          <DialogTitle>Confirm deletion</DialogTitle>
          <DialogContent>
            <div style={{ fontSize: 16, marginBottom: 8 }}>
              Are you sure you want to delete&nbsp;
              <b>{rowToDelete?.company_name}</b>?<br/>
              This action is irreversible.
            </div>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDeleteDialogOpen(false)}>
              Cancel
            </Button>
            <Button
              variant="contained"
              color="error"
              onClick={() => {
                if (rowToDelete && typeof rowToDelete.id === 'number') {
                  handleDeleteRow(rowToDelete.id);
                }
                setDeleteDialogOpen(false);
                setRowToDelete(null);
              }}
            >
              Delete
            </Button>
          </DialogActions>
        </Dialog>
        {/* Tag delete confirmation dialog */}
        <Dialog open={openDeleteTagDialog} onClose={() => setOpenDeleteTagDialog(false)}>
          <DialogTitle>Confirm tag deletion</DialogTitle>
          <DialogContent>
            <div style={{ fontSize: 16, marginBottom: 8 }}>
              Are you sure you want to delete the tag&nbsp;
              <b>{tagToDelete}</b>?<br/>
              This tag will be removed from all companies.
            </div>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDeleteTagDialog(false)}>
              Cancel
            </Button>
            <Button
              variant="contained"
              color="error"
              onClick={async () => {
                if (!tagToDelete) return;
                const tag = tagToDelete;
                const newTags = allTags.filter(t => t !== tag);
                setAllTags(newTags);
                setDialogTags(prev => prev.filter(t => t !== tag));
                setNewTagName("");
                setRows(prevRows => prevRows.map(r => ({ ...r, tags: Array.isArray(r.tags) ? r.tags.filter(t => t !== tag) : [] })));
                const db = getDatabase(firebaseApp);
                await import("firebase/database").then(({ ref, set, get }) => {
                  set(ref(db, "/tags"), newTags);
                  get(ref(db, "/Linkedin_list_with_country")).then(snapshot => {
                    const data = snapshot.val();
                    if (data) {
                      const updates: Record<string, any> = {};
                      Object.entries(data).forEach(([key, row]) => {
                        const typedRow = row as Row;
                        if (typedRow.tags && Array.isArray(typedRow.tags) && typedRow.tags.includes(tag)) {
                          updates[key] = { ...typedRow, tags: typedRow.tags.filter((t: string) => t !== tag) };
                        }
                      });
                      Object.entries(updates).forEach(([key, row]) => {
                        set(ref(db, `/Linkedin_list_with_country/${key}`), row);
                      });
                    }
                  });
                });
                setOpenDeleteTagDialog(false);
                setTagToDelete(null);
                setSnackbar({open: true, message: `Tag deleted`, severity: 'success'});
              }}
            >
              Delete
            </Button>
          </DialogActions>
        </Dialog>
        {/* Loader skeleton while loading */}
        {loading ? (
          <div style={{ padding: 32 }}>
            <Skeleton variant="rectangular" width="100%" height={48} style={{ marginBottom: 16 }} />
            <Skeleton variant="rectangular" width="100%" height={48} style={{ marginBottom: 16 }} />
            <Skeleton variant="rectangular" width="100%" height={48} />
          </div>
        ) : (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              maxHeight: "calc(100vh - 320px)",
              background: '#fff',
              borderRadius: 12,
              boxShadow: '0 2px 12px #1976d210',
              overflow: 'hidden',
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
              sx={{ minHeight: 400, fontSize: 15, border: 0, background: '#fff' }}
              getRowHeight={() => 'auto'}
              processRowUpdate={async (newRow, oldRow) => {
                try {
                  setRows(prev => prev.map((r, i) => i === newRow.id ? { ...newRow } : r));
                  const db = getDatabase(firebaseApp);
                  const { id, ...rowToSave } = newRow;
                  await import("firebase/database").then(({ ref, set }) =>
                    set(ref(db, `/Linkedin_list_with_country/${newRow.id}`), { ...rowToSave })
                  );
                  setSnackbar({open: true, message: 'Compagnie modifiée', severity: 'success'});
                } catch (e) {
                  setSnackbar({open: true, message: 'Erreur lors de la modification', severity: 'error'});
                }
                return newRow;
              }}
              onProcessRowUpdateError={error => {
                setSnackbar({open: true, message: 'Erreur lors de la sauvegarde', severity: 'error'});
                console.error('Error while saving to Firebase:', error);
              }}
            />
          </div>
        )}
      </List>
    </>
  );
}

// Utility function to generate a color from a tag
function getTagColor(tag: string) {
  // Normalize to ignore accents and case
  const norm = (str: string) => str.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase().trim();
  const tagNorm = norm(tag);
  if (tagNorm === 'amerique') {
    return 'hsl(0, 75%, 48%)'; // bright red
  }
  if (tagNorm === 'afrique subsaharienne') {
    return 'hsl(45, 90%, 52%)'; // golden yellow
  }
  if (tagNorm === 'amerique latine et caraibes') {
    return 'hsl(330, 80%, 70%)'; // pink
  }
  // Otherwise, varied color
  let hash = 0;
  for (let i = 0; i < tag.length; i++) {
    hash = tag.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = Math.abs(hash * 47) % 360;
  const sat = 55 + (Math.abs(hash * 31) % 35);
  const light = 42 + (Math.abs(hash * 61) % 16);
  return `hsl(${hue}, ${sat}%, ${light}%)`;
}
