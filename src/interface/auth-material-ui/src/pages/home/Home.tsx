import React from "react";
import { Box, Typography, Paper } from "@mui/material";
import Grid from "@mui/material/Grid";
import PeopleIcon from "@mui/icons-material/People";
import LocalAirportIcon from "@mui/icons-material/LocalAirport";
import { Link } from "react-router-dom";

const pages = [
  {
    label: "Users",
    icon: <PeopleIcon fontSize="large" color="primary" />,
    link: "/user",
  },
  {
    label: "Airlines",
    icon: <LocalAirportIcon fontSize="large" color="primary" />,
    link: "/airline",
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
      <Grid container spacing={3} justifyContent="center" mb={4} columns={12}>
        {pages.map((page) => (
          <Grid
            key={page.label}
            sx={{
              gridColumn: {
                xs: "span 12",
                sm: "span 6",
                md: "span 3",
              },
              display: "flex",
            }}
          >
            <Paper
              elevation={3}
              sx={{
                p: 3,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                textAlign: "center",
                textDecoration: "none",
                transition: "0.2s",
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