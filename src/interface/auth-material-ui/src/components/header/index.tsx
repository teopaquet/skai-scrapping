import DarkModeOutlined from "@mui/icons-material/DarkModeOutlined";
import LightModeOutlined from "@mui/icons-material/LightModeOutlined";
import AccountCircleOutlined from "@mui/icons-material/AccountCircleOutlined";
import MenuIcon from "@mui/icons-material/Menu";
import AppBar from "@mui/material/AppBar";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import React, { useContext } from "react";
import { HamburgerMenu, RefineThemedLayoutV2HeaderProps } from "@refinedev/mui";
import { ColorModeContext } from "../../contexts/color-mode";
import { useDrawer } from "../../contexts/drawer-context";

export const Header: React.FC<RefineThemedLayoutV2HeaderProps> = ({
  sticky = true,
}) => {
  const { mode, setMode } = useContext(ColorModeContext);
  const { drawerOpen, toggleDrawer } = useDrawer();

  // Retrieve the username directly from localStorage
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  return (
    <AppBar position={sticky ? "sticky" : "relative"}>
      <Toolbar>
        <Stack
          direction="row"
          width="100%"
          justifyContent="space-between"
          alignItems="center"
        >
          {/* Bouton burger pour ouvrir/fermer la barre latérale */}
          <IconButton
            color="inherit"
            onClick={toggleDrawer}
            aria-label={drawerOpen ? "Close sidebar" : "Open sidebar"}
            sx={{
              boxShadow: "none",
              outline: "none",
              padding: "8px",
              marginLeft: "8px",
            }}
          >
            <MenuIcon />
          </IconButton>

          {/* Section droite */}
          <Stack direction="row" alignItems="center" gap="16px">
            <IconButton
              color="inherit"
              onClick={setMode}
              aria-label="Toggle dark mode"
              sx={{
                boxShadow: "none",
                outline: "none",
              }}
            >
              {mode === "dark" ? <LightModeOutlined /> : <DarkModeOutlined />}
            </IconButton>

            {/* Display username */}
            <Stack direction="row" gap="8px" alignItems="center">
              <Typography variant="subtitle2" fontWeight="bold">
                {user.first_name || "Admin"}
              </Typography>
              <AccountCircleOutlined fontSize="large" />
            </Stack>
          </Stack>
        </Stack>
      </Toolbar>
    </AppBar>
  );
};
