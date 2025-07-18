import React from "react";
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

  return (
    <List>
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
          autoHeight
          initialState={{
            pagination: { paginationModel: { pageSize: 25, page: 0 } },
          }}
          pageSizeOptions={[25, 50, 100]}
        />
      </div>
    </List>
  );
};
