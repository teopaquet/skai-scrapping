import { Refine } from "@refinedev/core";
import { DevtoolsProvider } from "@refinedev/devtools";
import { RefineKbar, RefineKbarProvider } from "@refinedev/kbar";

import {
  ErrorComponent,
  RefineSnackbarProvider,
  ThemedLayoutV2,
  ThemedSiderV2,
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
import { ColorModeContextProvider } from "./contexts/color-mode";
import { LinkedinList } from "./pages/linkedin/list";
import { FleetList } from "./pages/fleet/list";
import { DrawerProvider } from "./contexts/drawer-context";
import { Header } from "./components/header";
import HomeIcon from "@mui/icons-material/Home";
import LocalAirportIcon from "@mui/icons-material/LocalAirport";
import LinkedInIcon from '@mui/icons-material/LinkedIn';


function App() {
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
                      meta: {
                        label: "Linkedin",
                        icon: <LinkedInIcon />,
                      },
                    },
                    {
                      name: "Airline's Linkedin",
                      list: "/linkedin",
                      create: "/linkedin/create",
                      edit: "/linkedin/edit/:id",
                      show: "/linkedin/show/:id",
                      meta: {
                        label: "Airline's Linkedin",
                        parent: "Linkedin",
                        canDelete: true,
                        icon: <LinkedInIcon />
                      },
                    },
                        {
                      name: "Employee's Linkedin",
                      list: "/employee",
                      create: "/employee/create",
                      edit: "/employee/edit/:id",
                      show: "/employee/show/:id",
                      meta: {
                        label: "Employee's Linkedin",
                        parent: "Linkedin",
                        canDelete: true,
                        icon: <LinkedInIcon />
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
                          Sider={(props) => (
                            <ThemedSiderV2
                              {...props}
                              Title={({ collapsed }) => (
                                <div style={{ display: "flex", alignItems: "center", gap: 8, padding: 16 }}>
                                  <img src="/logo_skai.svg" alt="Skai Visualizer" style={{ height: 32, width: 32 }} />
                                  {!collapsed && (
                                    <span style={{ fontWeight: "bold", fontSize: 18, color: "#1976d2", fontFamily: "Roboto, sans-serif" }}>
                                      Skai Visualizer
                                    </span>
                                  )}
                                </div>
                              )}
                            />
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
                        return `${resource.meta.label} | Skai Visualizer`;
                      }
                      return "Skai Visualizer";
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


