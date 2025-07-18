import { Authenticated, Refine } from "@refinedev/core";
import { DevtoolsProvider } from "@refinedev/devtools";
import { RefineKbar, RefineKbarProvider } from "@refinedev/kbar";

import {
  ErrorComponent,
  RefineSnackbarProvider,
  ThemedLayoutV2,
  useNotificationProvider,
} from "@refinedev/mui";

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
import { authProvider } from "./authProvider";
import { Header } from "./components/header";
import { ColorModeContextProvider } from "./contexts/color-mode";
import { ForgotPassword } from "./pages/forgotPassword";
import Login  from "./pages/Login";
import { Register } from "./pages/register";
import Typography from "@mui/material/Typography";
import React, { useState } from "react";
import { DrawerProvider } from "./contexts/drawer-context";
import SettingsIcon from "@mui/icons-material/Settings";
import PeopleIcon from "@mui/icons-material/People";
import HomeIcon from "@mui/icons-material/Home";
import FlightTakeoffIcon from "@mui/icons-material/FlightTakeoff";
import ConnectingAirportsIcon from '@mui/icons-material/ConnectingAirports';
import AirplanemodeActiveIcon from '@mui/icons-material/AirplanemodeActive';
import FlightClassIcon from '@mui/icons-material/FlightClass';
import LocalAirportIcon from "@mui/icons-material/LocalAirport";
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import LeaderboardIcon from '@mui/icons-material/Leaderboard';

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
                  authProvider={authProvider}
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
                      name: "users",
                      list: "/user",
                      create: "/user/create",
                      edit: "/user/edit/:id",
                      show: "/user/show/:id",
                      meta: {
                        canDelete: true,
                        icon: <PeopleIcon />
                      },
                    },
                    {
                      name: "airline",
                      list: "/airline",
                      create: "/airline/create",
                      edit: "/airline/edit/:id",
                      show: "/airline/show/:id",
                      meta: {
                        label: "Airline",
                        icon: <LocalAirportIcon />,
                      },
                    },
                    {
                      name: "configuration",
                      meta: {
                        label: "Configuration",
                        icon: <SettingsIcon />,
                      },
                    },
                    {
                      name: "activity-type",
                      list: "/activity-type",
                      create: "/activity-type/create",
                      edit: "/activity-type/edit/:id",
                      show: "/activity-type/show/:id",
                      meta: {
                        parent: "configuration",
                        label: "Activity Types",
                        icon: <FlightClassIcon />,
                      },
                    },
                    {
                      name: "aircraft-type",
                      list: "/aircraft-type",
                      create: "/aircraft-type/create",
                      edit: "/aircraft-type/edit/:id",
                      show: "/aircraft-type/show/:id",
                      meta: {
                        parent: "configuration",
                        label: "Aircraft Types",
                        icon: <AirplanemodeActiveIcon />,
                      },
                    },
                    {
                      name: "flight-type",
                      list: "/flight-type",
                      create: "/flight-type/create",
                      edit: "/flight-type/edit/:id",
                      show: "/flight-type/show/:id",
                      meta: {
                        parent: "configuration",
                        label: "Flight Types",
                        icon: <FlightTakeoffIcon />,
                      },
                    },
                    {
                      name: "pairing-type",
                      list: "/pairing-type",
                      create: "/pairing-type/create",
                      edit: "/pairing-type/edit/:id",
                      show: "/pairing-type/show/:id",
                      meta: {
                        parent: "configuration",
                        label: "Pairing Types",
                        icon: <ConnectingAirportsIcon />,
                      },
                    },
                    {
                      name: "roster-activity-type",
                      list: "/roster-activity-type",
                      create: "/roster-activity-type/create",
                      edit: "/roster-activity-type/edit/:id",
                      show: "/roster-activity-type/show/:id",
                      meta: {
                        parent: "configuration",
                        label: "Roster Activity Types",
                        icon: <FlightTakeoffIcon />,
                      },
                    },
                    {
                      name: "schedule",
                      list: "/schedule",
                      meta: {
                        label: "Schedule",
                        icon: <CalendarMonthIcon />,
                        canDelete: false,
                        canEdit: false,
                        canCreate: false,
                      },
                    },
                    {
                      name: "data",
                      meta: {
                        label: "Data",
                        icon: <LeaderboardIcon />,
                      },
                    },
                    {
                      name: "crew",
                      list: "/crew",
                      meta: {
                        parent: "data",
                        label: "Crew",
                        icon: <PeopleIcon />,
                        filterRequired: true,
                      },
                    },
                    {
                      name: "flight",
                      list: "/flight",
                      show: "/flight/show/:id",
                      meta: {
                        parent: "data",
                        label: "Flight",
                        icon: <FlightTakeoffIcon />,
                        filterRequired: true,
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
                        <Authenticated
                          key="authenticated-inner"
                          fallback={<CatchAllNavigate to="/login" />}
                        >
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
                                {drawerOpen ? "Skai Admin" : "SA"}
                              </Typography>
                            )}
                          >
                            <Outlet />
                          </ThemedLayoutV2>
                        </Authenticated>
                      }
                    >


                      {/* Route pour les utilisateurs */}
                      {/* <Route path="/user">
                        <Route index element={<UserList />} /> */}
                        {/* <Route path="create" element={<UserCreate />} />
                        <Route path="edit/:id" element={<UserEdit />} /> */}
                        {/* <Route path="show/:id" element={<UserShow />} /> */}
                      {/* </Route> */}

                      

                      <Route path="*" element={<ErrorComponent />} />
                    </Route>
                    <Route
                      element={
                        <Authenticated
                          key="authenticated-outer"
                          fallback={<Outlet />}
                        >
                          <NavigateToResource />
                        </Authenticated>
                      }
                    >
                      <Route path="/login" element={<Login />} />
                      <Route path="/register" element={<Register />} />
                      <Route
                        path="/forgot-password"
                        element={<ForgotPassword />}
                      />
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