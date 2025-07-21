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
  CatchAllNavigate,
  DocumentTitleHandler,
  NavigateToResource,
  UnsavedChangesNotifier,
} from "@refinedev/react-router";
import dataProvider from "./services/dataProvider";
import { BrowserRouter, Outlet, Route, Routes } from "react-router-dom";
import { Header } from "./components/header";
import { ColorModeContextProvider } from "./contexts/color-mode";
import { LinkedinList } from "./pages/linkedin/list";
// import { LinkedinCreate } from "./pages/linkedin/create";
// import { LinkedinEdit } from "./pages/linkedin/edit";
// import { LinkedinShow } from "./pages/linkedin/show";
import { FleetList } from "./pages/fleet/list";
// import { FleetCreate } from "./pages/fleet/create";
// import { FleetEdit } from "./pages/fleet/edit";
// import { FleetShow } from "./pages/fleet/show";
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
                  
                    <Route
                      
                    >
                      <Route path="/" element={<Home />} />

                      {/* Linkedin routes */}
                      <Route path="/linkedin">
                        <Route index element={<LinkedinList />} />
                        {/* <Route path="create" element={<LinkedinCreate />} /> */}
                        {/* <Route path="edit/:id" element={<LinkedinEdit />} /> */}
                        {/* <Route path="show/:id" element={<LinkedinShow />} /> */}
                      </Route>

                      {/* Fleet routes (décommentez et créez les composants si besoin) */}
                      {
                      <Route path="/fleet">
                        <Route index element={<FleetList />} />
                        {/* <Route path="create" element={<FleetCreate />} />
                        <Route path="edit/:id" element={<FleetEdit />} />
                        <Route path="show/:id" element={<FleetShow />} /> */}
                      </Route>
                      }

                      <Route path="*" element={<ErrorComponent />} />
                    </Route>
                    

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