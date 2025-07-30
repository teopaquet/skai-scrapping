import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import React from "react";
import Snackbar from "@mui/material/Snackbar";
import MuiAlert from "@mui/material/Alert";
import Skeleton from "@mui/material/Skeleton";
import { List } from "@refinedev/mui";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";
import TextField from "@mui/material/TextField";
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
  employee_name: string;
  linkedin_url: string;
  description: string;
  email?: string;
  phone_number?: string;
  company: string;
  location?: string;
  roles?: string[];
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
  // Company selector (autocomplete)
  // State for creation
  const [openCreateDialog, setOpenCreateDialog] = React.useState(false);
  const [newEmployee, setNewEmployee] = React.useState<Row>({
    employee_name: '',
    linkedin_url: '',
    description: '',
    email: '',
    phone_number: '',
    company: '',
    location: '',
    roles: [],
  });
  const firstInputRef = React.useRef<HTMLInputElement>(null);
  React.useEffect(() => {
    if (openCreateDialog && firstInputRef.current) {
      setTimeout(() => firstInputRef.current?.focus(), 200);
    }
  }, [openCreateDialog]);

  // Function to create a new employee
  const handleCreateEmployee = async () => {
    if (!newEmployee.employee_name.trim() || !newEmployee.company.trim()) {
      setSnackbar({open: true, message: 'Name and company required', severity: 'warning'});
      return;
    }
    try {
      setRows(prev => [...prev, { ...newEmployee }]);
      const db = getDatabase(firebaseApp);
      const newId = rows.length;
      await import("firebase/database").then(({ ref, set }) =>
        set(ref(db, `/Employee_list_with_country/${newId}`), { ...newEmployee })
      );
      setOpenCreateDialog(false);
      setNewEmployee({ employee_name: '', linkedin_url: '', description: '', email: '', phone_number: '', company: '', location: '', roles: [] });
      setSnackbar({open: true, message: 'Employee created', severity: 'success'});
      setTimeout(() => window.scrollTo({top: 0, behavior: 'smooth'}), 200);
      setTimeout(() => window.location.reload(), 800);
    } catch (e) {
      setSnackbar({open: true, message: 'Error while creating', severity: 'error'});
    }
  };
  // Function to handle delete employee
  const handleDeleteRow = async (rowId: number) => {
      try {
        setRows(prev => prev.filter((_, i) => i !== rowId));
        const db = getDatabase(firebaseApp);
        await import("firebase/database").then(({ ref, remove }) =>
          remove(ref(db, `/Employee_list_with_country/${rowId}`))
        );
        setSnackbar({open: true, message: 'Company deleted', severity: 'success'});
        setTimeout(() => window.scrollTo({top: 0, behavior: 'smooth'}), 200);
        setTimeout(() => window.location.reload(), 800);
      } catch (e) {
        setSnackbar({open: true, message: 'Error while deleting', severity: 'error'});
      }
    };
  const [selectedCompany, setSelectedCompany] = React.useState<string>("");
  const [companyOptions, setCompanyOptions] = React.useState<string[]>([]);
  // List of global tags
  const [allRoles, setAllRoles] = React.useState<string[]>([]);
  // For role creation in progress
  const [roleInput, setRoleInput] = React.useState("");
  // Dialog for role management (per row)
  const [openRoleDialog, setOpenRoleDialog] = React.useState(false);
  const [selectedRow, setSelectedRow] = React.useState<Row | null>(null);
  const [dialogRoles, setDialogRoles] = React.useState<string[]>([]);
  const [newRoleName, setNewRoleName] = React.useState("");
  // Dialog for global role management
  const [openManageRolesDialog, setOpenManageRolesDialog] = React.useState(false);

  // For delete confirmation
  const [deleteDialogOpen, setDeleteDialogOpen] = React.useState(false);
  const [rowToDelete, setRowToDelete] = React.useState<Row | null>(null);

  // Add state for role delete confirmation
  const [openDeleteRoleDialog, setOpenDeleteRoleDialog] = React.useState(false);
  const [RoleToDelete, setRoleToDelete] = React.useState<string | null>(null);

  React.useEffect(() => {
    const db = getDatabase(firebaseApp);
    async function fetchRows() {
      try {
        const snapshot = await get(ref(db, "/Employee_list_with_country"));
        const data = snapshot.val();
        const list: Row[] = Array.isArray(data) ? data : (data ? Object.values(data) : []);
        setRows(list);
      } catch (e) {
        setSnackbar({open: true, message: 'Error loading employees', severity: 'error'});
      } finally {
        setLoading(false);
      }
    }
    async function fetchCompanies() {
      try {
        const snapshot = await get(ref(db, "/Linkedin_list_with_country"));
        const data = snapshot.val();
        const setCompanies = new Set<string>();
        const list = Array.isArray(data) ? data : (data ? Object.values(data) : []);
        list.forEach((row: any) => {
          if (row && row.company_name) setCompanies.add(row.company_name);
        });
        setCompanyOptions(Array.from(setCompanies).sort());
      } catch (e) {
        setSnackbar({open: true, message: 'Error loading companies', severity: 'error'});
      }
    }
    async function fetchRoles() {
      try {
        const snapshot = await get(ref(db, "/employee_roles"));
        let data = snapshot.val();
        if (!data) {
          // If roles section missing, create it as empty array
          await import("firebase/database").then(({ ref, set }) =>
            set(ref(db, "/employee_roles"), [])
          );
          setAllRoles([]);
        } else if (Array.isArray(data)) setAllRoles(data.filter(Boolean));
        else if (typeof data === 'object') setAllRoles((Object.values(data).filter(Boolean) as string[]));
        else setAllRoles([]);
      } catch (e) {
        setSnackbar({open: true, message: 'Error loading roles', severity: 'error'});
      }
    }
    fetchRows();
    fetchCompanies();
    fetchRoles();
  }, []);

  const columns = React.useMemo<GridColDef<Row>[]>(
    () => [
      {
        field: "employee_name",
        headerName: "Employee Name",
        minWidth: 200,
        flex: 1,
        editable: true,
      },
      {
        field: "roles",
        headerName: "Roles",
        minWidth: 200,
        flex: 1,
        editable: false,
        renderCell: (params) => {
          const roles = Array.isArray(params.value) ? params.value : [];
          return (
            <span
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-start',
                width: '100%',
                height: '100%',
                gap: roles.length > 0 ? 8 : 0,
              }}
            >
              {roles.length > 0 ? (
                <span
                  style={{ display: 'flex', gap: 6, flexWrap: 'wrap', cursor: 'pointer', userSelect: 'none', alignItems: 'center' }}
                  onClick={e => {
                    e.stopPropagation();
                    setSelectedRow(params.row);
                    setDialogRoles(roles);
                    setOpenRoleDialog(true);
                  }}
                  title="Manage roles"
                >
                  {roles.map((role, idx) => (
                    <Chip
                      key={role + idx}
                      label={role}
                      size="small"
                      style={{
                        borderRadius: 16,
                        fontWeight: 500,
                        background: getRoleColor(role),
                        color: '#fff',
                        letterSpacing: 0.2,
                        boxShadow: '0 1px 4px #0001',
                        fontSize: 13,
                        marginRight: idx === roles.length - 1 ? 0 : 0,
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
                    setDialogRoles(roles);
                    setOpenRoleDialog(true);
                  }}
                  title="Add or edit roles"
                >
                  <AddIcon fontSize="small" style={{ color: '#555', position: 'relative' }} />
                </Button>
              )}
            </span>
          );
        },
      },
      {
        field: "company",
        headerName: "Company",
        minWidth: 200,
        flex: 1,
        editable: true,
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
        field: "location",
        headerName: "Location",
        minWidth: 120,
        flex: 0.5,
        editable: true,
      },
      {
        field: "email",
        headerName: "Email",
        minWidth: 200,
        flex: 1,
        editable: true,
      },
      {
        field: "phone_number",
        headerName: "Phone",
        minWidth: 120,
        flex: 0.5,
        editable: true,
      },
      {
        field: "description",
        headerName: "Description",
        minWidth: 180,
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
            title="Delete employee"
            style={{ minWidth: 0, padding: 4 }}
          >
            <DeleteIcon fontSize="small" />
          </Button>
        ),
      },
    ],
    [allRoles]
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

  // Pagination state with persistence
  const getInitialPagination = () => {
    if (typeof window === 'undefined') return { pageSize: 25, page: 0 };
    const saved = localStorage.getItem('employee_pagination');
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
  React.useEffect(() => {
    if (typeof window === 'undefined') return;
    localStorage.setItem('employee_pagination', JSON.stringify(paginationModel));
  }, [paginationModel]);


  // Filter rows by selected company
  const filteredRows = rows
    .map((row, i) => ({ ...row, id: i }))
    .filter(row => {
      if (!selectedCompany) return true;
      return row.company === selectedCompany;
    });

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
        <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
          <Autocomplete
            options={["All companies", ...companyOptions]}
            value={selectedCompany || "All companies"}
            onChange={(_, newValue) => {
              // If cleared or "All companies" selected, remove filter
              if (!newValue || newValue === "All companies") {
                setSelectedCompany("");
              } else {
                setSelectedCompany(newValue);
              }
            }}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Select company"
                placeholder="Type to search..."
                style={{ minWidth: 220 }}
              />
            )}
            clearOnEscape
            isOptionEqualToValue={(option, value) => option === value}
            autoHighlight
            // Allow clearing selection to remove filter
            disableClearable={false}
          />
          <div style={{ flex: 1 }} />
          <Button
            variant="outlined"
            color="primary"
            onClick={() => setOpenManageRolesDialog(true)}
            style={{ fontWeight: 500, fontSize: 14 }}
          >
            Manage Roles
          </Button>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={() => setOpenCreateDialog(true)}
            style={{ whiteSpace: 'nowrap', fontWeight: 600, fontSize: 15, boxShadow: '0 2px 8px #1976d220' }}
          >
            Add an employee
          </Button>
        </div>
         {/* Global Manage Tags dialog */}
                <Dialog open={openManageRolesDialog} onClose={() => setOpenManageRolesDialog(false)} TransitionProps={{ appear: true }}>
                  <DialogTitle>Manage all Roles</DialogTitle>
                  <DialogContent>
                    <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 12 }}>
                      <TextField
                        label="New Role"
                        size="small"
                        value={newRoleName}
                        onChange={e => setNewRoleName(e.target.value)}
                        onKeyDown={e => {
                          if (e.key === 'Enter' && newRoleName.trim()) {
                            if (!allRoles.includes(newRoleName.trim())) {
                              const newRoles = [...allRoles, newRoleName.trim()];
                              setAllRoles(newRoles);
                              const db = getDatabase(firebaseApp);
                              import("firebase/database").then(({ ref, set }) =>
                                set(ref(db, "/Roles"), newRoles)
                              );
                            }
                            setNewRoleName("");
                          }
                        }}
                        placeholder="Add a Role..."
                      />
                      <Button onClick={() => {
                        if (newRoleName.trim()) {
                          if (!allRoles.includes(newRoleName.trim())) {
                            const newRoles = [...allRoles, newRoleName.trim()];
                            setAllRoles(newRoles);
                            const db = getDatabase(firebaseApp);
                            import("firebase/database").then(({ ref, set }) =>
                              set(ref(db, "/Roles"), newRoles)
                            );
                          }
                          setNewRoleName("");
                        }
                      }} variant="contained" size="small">Add</Button>
                    </div>
                    <div style={{ marginTop: 8, fontSize: 13, color: '#888' }}>
                      <b>Existing Roles:</b>
                      <span style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 6 }}>
                        {allRoles.map((role, idx) => (
                          <Chip
                            key={role + idx}
                            label={role}
                            size="small"
                            style={{
                              borderRadius: 16,
                              fontWeight: 500,
                              background: getRoleColor(role),
                              color: '#fff',
                              letterSpacing: 0.2,
                              boxShadow: '0 1px 4px #0001',
                              fontSize: 13
                            }}
                            onDelete={() => {
                              setRoleToDelete(role);
                              setOpenDeleteRoleDialog(true);
                            }}
                          />
                        ))}
                      </span>
                    </div>
                  </DialogContent>
                  <DialogActions>
                    <Button onClick={() => setOpenManageRolesDialog(false)}>Close</Button>
                  </DialogActions>
                </Dialog>
        {/* Delete confirmation dialog */}
                <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
                  <DialogTitle>Confirm deletion</DialogTitle>
                  <DialogContent>
                    <div style={{ fontSize: 16, marginBottom: 8 }}>
                      Are you sure you want to delete&nbsp;
                      <b>{rowToDelete?.employee_name}</b>?<br/>
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
        {/* Dialog to create a new employee with transition and focus */}
        <Dialog open={openCreateDialog} onClose={() => setOpenCreateDialog(false)} TransitionProps={{ appear: true }}>
          <DialogTitle>Create a new employee</DialogTitle>
          <DialogContent>
            <TextField
              label="Employee name"
              value={newEmployee.employee_name}
              onChange={e => setNewEmployee(c => ({ ...c, employee_name: e.target.value }))}
              fullWidth
              margin="dense"
              inputRef={firstInputRef}
              required
              autoFocus
            />
            <TextField
              label="LinkedIn URL"
              value={newEmployee.linkedin_url}
              onChange={e => setNewEmployee(c => ({ ...c, linkedin_url: e.target.value }))}
              fullWidth
              margin="dense"
              placeholder="https://linkedin.com/in/..."
            />
            <TextField
              label="Description"
              value={newEmployee.description}
              onChange={e => setNewEmployee(c => ({ ...c, description: e.target.value }))}
              fullWidth
              margin="dense"
              multiline
              minRows={2}
            />
            <TextField
              label="Email"
              value={newEmployee.email}
              onChange={e => setNewEmployee(c => ({ ...c, email: e.target.value }))}
              fullWidth              
            />
            <TextField
              label="Phone number"
              value={newEmployee.phone_number}
              onChange={e => setNewEmployee(c => ({ ...c, phone_number: e.target.value }))}
              fullWidth
              margin="dense"
            />  
            <Autocomplete
              multiple
              options={companyOptions}
              value={newEmployee.company ? [newEmployee.company] : []}
              onChange={(_, newValue) => setNewEmployee(c => ({ ...c, company: newValue[0] || '' }))}
              renderTags={(tagValue, getTagProps) =>
                tagValue.map((option, index) => (
                  <Chip variant="outlined" label={option} {...getTagProps({ index })} key={option} />
                ))
              }
              renderInput={params => (
                <TextField {...params} label="Company" margin="dense" fullWidth required variant="standard" />
              )}
              style={{ marginBottom: 8 }}
              freeSolo
              filterSelectedOptions
              autoHighlight
              autoSelect
              openOnFocus
            />
            <TextField
              label="Location"
              value={newEmployee.location}
              onChange={e => setNewEmployee(c => ({ ...c, location: e.target.value }))}
              fullWidth
              margin="dense"
            />
            <Autocomplete
              multiple
              options={allRoles}
              value={newEmployee.roles || []}
              onChange={(_, newValue) => setNewEmployee(c => ({ ...c, roles: newValue }))}
              renderTags={(roleValue, getTagProps) =>
                roleValue.map((option, index) => (
                  <Chip variant="outlined" label={option} {...getTagProps({ index })} key={option} />
                ))
              }
              renderInput={paramsInput => (
                <TextField {...paramsInput} variant="standard" label="Roles" />
              )}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenCreateDialog(false)}>Cancel</Button>
            <Button variant="contained" onClick={handleCreateEmployee} color="primary">Create</Button>
          </DialogActions>
        </Dialog>
        {/* Tag delete confirmation dialog */}
                <Dialog open={openDeleteRoleDialog} onClose={() => setOpenDeleteRoleDialog(false)}>
                  <DialogTitle>Confirm Role deletion</DialogTitle>
                  <DialogContent>
                    <div style={{ fontSize: 16, marginBottom: 8 }}>
                      Are you sure you want to delete the Role&nbsp;
                      <b>{RoleToDelete}</b>?<br/>
                      This Role will be removed from all companies.
                    </div>
                  </DialogContent>
                  <DialogActions>
                    <Button onClick={() => setOpenDeleteRoleDialog(false)}>
                      Cancel
                    </Button>
                    <Button
                      variant="contained"
                      color="error"
                      onClick={async () => {
                        if (!RoleToDelete) return;
                        const Role = RoleToDelete;
                        const newRoles = allRoles.filter(t => t !== Role);
                        setAllRoles(newRoles);
                        setDialogRoles(prev => prev.filter(t => t !== Role));
                        setNewRoleName("");
                        setRows(prevRows => prevRows.map(r => ({ ...r, Roles: Array.isArray(r.roles) ? r.roles.filter(t => t !== Role) : [] })));
                        const db = getDatabase(firebaseApp);
                        await import("firebase/database").then(({ ref, set, get }) => {
                          set(ref(db, "/Roles"), newRoles);
                          get(ref(db, "/Linkedin_list_with_country")).then(snapshot => {
                            const data = snapshot.val();
                            if (data) {
                              const updates: Record<string, any> = {};
                              Object.entries(data).forEach(([key, row]) => {
                                const typedRow = row as Row;
                                if (typedRow.roles && Array.isArray(typedRow.roles) && typedRow.roles.includes(Role)) {
                                  updates[key] = { ...typedRow, Roles: typedRow.roles.filter((t: string) => t !== Role) };
                                }
                              });
                              Object.entries(updates).forEach(([key, row]) => {
                                set(ref(db, `/Linkedin_list_with_country/${key}`), row);
                              });
                            }
                          });
                        });
                        setOpenDeleteRoleDialog(false);
                        setRoleToDelete(null);
                        setSnackbar({open: true, message: `Tag deleted`, severity: 'success'});
                      }}
                    >
                      Delete
                    </Button>
                  </DialogActions>
                </Dialog>
        {/* Per-employee Manage Roles dialog */}
        <Dialog open={openRoleDialog} onClose={() => setOpenRoleDialog(false)} TransitionProps={{ appear: true }}>
          <DialogTitle>Manage roles for {selectedRow?.employee_name}</DialogTitle>
          <DialogContent>
            <div style={{ marginBottom: 12 }}>
              <Autocomplete
                multiple
                options={allRoles}
                value={dialogRoles}
                onChange={(_, newValue) => setDialogRoles(newValue)}
                renderTags={(roleValue, getTagProps) =>
                  roleValue.map((option, index) => (
                    <Chip variant="outlined" label={option} {...getTagProps({ index })} key={option} />
                  ))
                }
                renderInput={paramsInput => (
                  <TextField {...paramsInput} variant="standard" label="Roles to assign" />
                )}
              />
            </div>
            <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 4 }}>
              <TextField
                label="New role"
                size="small"
                value={newRoleName}
                onChange={e => setNewRoleName(e.target.value)}
                onKeyDown={async e => {
                  if (e.key === 'Enter' && newRoleName.trim()) {
                    if (!allRoles.includes(newRoleName.trim())) {
                      const newRoles = [...allRoles, newRoleName.trim()];
                      setAllRoles(newRoles);
                      setDialogRoles(prev => [...prev, newRoleName.trim()]);
                      const db = getDatabase(firebaseApp);
                      await import("firebase/database").then(({ ref, set }) =>
                        set(ref(db, "/employee_roles"), newRoles)
                      );
                    } else if (!dialogRoles.includes(newRoleName.trim())) {
                      setDialogRoles(prev => [...prev, newRoleName.trim()]);
                    }
                    setNewRoleName("");
                  }
                }}
                placeholder="Add a role..."
              />
              <Button onClick={async () => {
                if (newRoleName.trim()) {
                  if (!allRoles.includes(newRoleName.trim())) {
                    const newRoles = [...allRoles, newRoleName.trim()];
                    setAllRoles(newRoles);
                    setDialogRoles(prev => [...prev, newRoleName.trim()]);
                    const db = getDatabase(firebaseApp);
                    await import("firebase/database").then(({ ref, set }) =>
                      set(ref(db, "/employee_roles"), newRoles)
                    );
                  } else if (!dialogRoles.includes(newRoleName.trim())) {
                    setDialogRoles(prev => [...prev, newRoleName.trim()]);
                  }
                  setNewRoleName("");
                }
              }} variant="contained" size="small">Add</Button>
            </div>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenRoleDialog(false)}>Cancel</Button>
            <Button variant="contained" onClick={async () => {
              if (!selectedRow) return;
              setRows(prev => prev.map(r => r === selectedRow ? { ...r, roles: dialogRoles } : r));
              const db = getDatabase(firebaseApp);
              const { id, ...rowToSave } = { ...selectedRow, roles: dialogRoles };
              await import("firebase/database").then(({ ref, set }) =>
                set(ref(db, `/Employee_list_with_country/${selectedRow.id}`), { ...rowToSave })
              );
              setOpenRoleDialog(false);
              setSnackbar({open: true, message: 'Roles updated', severity: 'success'});
              setTimeout(() => window.scrollTo({top: 0, behavior: 'smooth'}), 200);
              setTimeout(() => window.location.reload(), 800);
            }}>Save</Button>
          </DialogActions>
        </Dialog>
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
            />
          </div>
        )}
      </List>
    </>

  );
};

// Utility function to generate a color from a tag
export default EmployeeList;
function getRoleColor(role: string) {
  // Normalize to ignore accents and case
  const norm = (str: string) => str.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase().trim();
  const roleNorm = norm(role);
  if (roleNorm === 'amerique') {
    return 'hsl(0, 75%, 48%)'; // bright red
  }
  if (roleNorm === 'afrique subsaharienne') {
    return 'hsl(45, 90%, 52%)'; // golden yellow
  }
  if (roleNorm === 'amerique latine et caraibes') {
    return 'hsl(330, 80%, 70%)'; // pink
  }
  // Otherwise, varied color
  let hash = 0;
  for (let i = 0; i < role.length; i++) {
    hash = role.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = Math.abs(hash * 47) % 360;
  const sat = 55 + (Math.abs(hash * 31) % 35);
  const light = 42 + (Math.abs(hash * 61) % 16);
  return `hsl(${hue}, ${sat}%, ${light}%)`;
}
