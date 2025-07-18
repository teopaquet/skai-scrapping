import React, { useState } from "react";
import axios from "axios";
import { Box, Button, TextField, Typography } from "@mui/material";

const Login: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async () => {
    try {
      const response = await axios.post(
        "https://staging-api.skai-tech.fr/auth/token",
        new URLSearchParams({
          grant_type: "password",
          username,
          password,
          scope: "",
          client_id: "string",
          client_secret: "string",
        }),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            accept: "application/json",
          },
        }
      );

      console.log("Login Response Data:", response.data);

      // Store the token in localStorage
      localStorage.setItem("refine-auth", response.data.access_token);

      // Store first_name if available
      if (response.data.user) {
        localStorage.setItem("user", JSON.stringify(response.data.user));
      }

      // Redirect the user after successful login
      window.location.href = "/";
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        console.error("Login failed:", err.response?.data || err.message);
        setError("Invalid username or password.");
      } else {
        console.error("An unexpected error occurred:", err);
        setError("An unexpected error occurred.");
      }
      console.error("Login failed:", err);
      setError("Invalid username or password.");
    }
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      height="100vh"
    >
      <Typography variant="h4" mb={2}>
        Login
      </Typography>
      <Box width="300px">
        <TextField
          fullWidth
          label="Username"
          variant="outlined"
          margin="normal"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <TextField
          fullWidth
          label="Password"
          type="password"
          variant="outlined"
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && (
          <Typography color="error" mt={1}>
            {error}
          </Typography>
        )}
        <Button
          fullWidth
          variant="contained"
          color="primary"
          onClick={handleLogin}
          sx={{ mt: 2 }}
        >
          Login
        </Button>
      </Box>
    </Box>
  );
};

export default Login;