import React, { createContext, useContext, useState } from "react";

const DrawerContext = createContext({
  drawerOpen: true,
  toggleDrawer: () => {},
});

export const useDrawer = () => useContext(DrawerContext);

export const DrawerProvider = ({ children }: { children: React.ReactNode }) => {
  const [drawerOpen, setDrawerOpen] = useState(true);
  const toggleDrawer = () => setDrawerOpen((prev) => !prev);

  return (
    <DrawerContext.Provider value={{ drawerOpen, toggleDrawer }}>
      {children}
    </DrawerContext.Provider>
  );
};
