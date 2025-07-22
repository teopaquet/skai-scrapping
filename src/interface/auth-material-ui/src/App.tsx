import { Authenticated, Refine } from "@refinedev/core";
import { DevtoolsProvider } from "@refinedev/devtools";
import { RefineKbar, RefineKbarProvider } from "@refinedev/kbar";

import {
  ErrorComponent,
  RefineSnackbarProvider,
  ThemedLayoutV2,
  useNotificationProvider,
} from "@refinedev/mui";

import { Home } from "./pages/home";
import CssBaseline from "@mui/material/CssBaseline";
import GlobalStyles from "@mui/material/GlobalStyles";
import routerBindings, {
  DocumentTitleHandler,
  UnsavedChangesNotifier,
} from "@refinedev/react-router";
import dataProvider from "./services/dataProvider";
import { BrowserRouter, Outlet, Route, Routes } from "react-router-dom";
import { Header } from "./components/header";
import { ColorModeContextProvider } from "./contexts/color-mode";
import { LinkedinList } from "./pages/linkedin/list";
import { FleetList } from "./pages/fleet/list";
import Typography from "@mui/material/Typography";
import React, { useState } from "react";
import { DrawerProvider } from "./contexts/drawer-context";
import PeopleIcon from "@mui/icons-material/People";
import HomeIcon from "@mui/icons-material/Home";
import LocalAirportIcon from "@mui/icons-material/LocalAirport";


function App() {
  const [drawerOpen] = useState(true); // État pour la barre latérale

  return (
    <BrowserRouter>
      <RefineKbarProvider>
        <ColorModeContextProvider>
          <CssBaseline />
          <GlobalStyles styles={{ html: { WebkitFontSmoothing: "auto" } }} />
          <RefineSnackbarProvider>
            <DevtoolsProvider>
              <DrawerProvider>
                <Refine
                  dataProvider={dataProvider()}
                  notificationProvider={useNotificationProvider}
                  routerProvider={routerBindings}
                  resources={[
                    {
                      name: "home",
                      list: "/",
                      meta: {
                        label: "Home",
                        icon: <HomeIcon />
                      },
                    },
                    {
                      name: "Linkedin",
                      list: "/linkedin",
                      create: "/linkedin/create",
                      edit: "/linkedin/edit/:id",
                      show: "/linkedin/show/:id",
                      meta: {
                        canDelete: true,
                        icon: <PeopleIcon />
                      },
                    },
                    {
                      name: "Fleet",
                      list: "/fleet",
                      create: "/fleet/create",
                      edit: "/fleet/edit/:id",
                      show: "/fleet/show/:id",
                      meta: {
                        label: "Fleets",
                        icon: <LocalAirportIcon />,
                      },
                    },
                  ]}
                  options={{
                    syncWithLocation: true,
                    warnWhenUnsavedChanges: true,
                    useNewQueryKeys: true,
                    projectId: "7zfUrY-9Qa6Va-R43BVg",
                  }}
                >
                  <Routes>
                    <Route
                      element={
                        <ThemedLayoutV2
                          Header={Header}
                          Title={() => (
                            <Typography
                              variant="h6"
                              sx={{
                                color: "primary.main",
                                fontWeight: "bold",
                                fontSize: drawerOpen ? "1.5rem" : "1rem",
                                fontFamily: "Roboto, sans-serif",
                                whiteSpace: "nowrap",
                                overflow: "hidden",
                              }}
                            >
                              {drawerOpen ? "Skai Visualizer" : "SV"}
                            </Typography>
                          )}
                        >
                          <Outlet />
                        </ThemedLayoutV2>
                      }
                    >
                      <Route path="/" element={<Home />} />
                      <Route path="/linkedin">
                        <Route index element={<LinkedinList />} />               
                        {/* <Route path="show/:id" element={<LinkedinShow />} /> */}
                      </Route>
                      <Route path="/fleet">
                        <Route index element={<FleetList />} />
                        {/* <Route path="show/:id" element={<FleetShow />} /> */}
                      </Route>
                      <Route path="*" element={<ErrorComponent />} />
                    </Route>
                  </Routes>
                  <RefineKbar />
                  <UnsavedChangesNotifier />
                  <DocumentTitleHandler
                    handler={({ resource }) => {
                      if (resource?.meta?.label) {
                        return `${resource.meta.label} | Skai Admin`;
                      }
                      return "Skai Admin";
                    }}
                  />
                </Refine>
              </DrawerProvider>
            </DevtoolsProvider>
          </RefineSnackbarProvider>
        </ColorModeContextProvider>
      </RefineKbarProvider>
    </BrowserRouter>
  );
}

export default App;