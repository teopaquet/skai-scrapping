import React from "react";
import { Box, Typography, Paper } from "@mui/material";
import Grid from "@mui/material/Grid";
import LocalAirportIcon from "@mui/icons-material/LocalAirport";
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import { Link } from "react-router-dom";

const pages = [
  {
    label: "Linkedin",
    icon: <LinkedInIcon fontSize="large" color="primary" />,
    link: "/linkedin",
    
  },
  {
    label: "Fleets",
    icon: <LocalAirportIcon fontSize="large" color="primary" />,
    link: "/fleet",
  },

];

const Home: React.FC = () => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="100vh"
      bgcolor="background.default"
      px={2}
    >
      <Typography variant="h3" mb={2}>
        Welcome to Skai Visualizer
      </Typography>
      <Typography variant="body1" mb={4}>
        Check airline's fleet, Linkedin, and more with ease.
      </Typography>
      <Grid container spacing={1} justifyContent="center" mb={4} columns={12}>
        {pages.map((page) => (
          <Grid
            key={page.label}
            item
            xs={12}
            sm={6}
            md={3}
            sx={{ display: "flex", justifyContent: "center" }}
          >
            <Paper
              elevation={3}
              sx={{
                width: 180,
                height: 120,
                p: 2,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                textAlign: "center",
                textDecoration: "none",
                transition: "0.2s",
                borderRadius: 50,
                bgcolor: "background.paper",
                boxShadow: 8,
                gap: 1,
                "&:hover": {
                  boxShadow: 6,
                  bgcolor: "action.hover",
                  textDecoration: "none",
                },
              }}
              component={Link}
              to={page.link}
            >
              {page.icon}
              <Typography variant="subtitle1" mt={1}>
                {page.label}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Home;