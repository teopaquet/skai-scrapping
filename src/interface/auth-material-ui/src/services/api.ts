// src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://staging-api.skai-tech.fr', // URL de base correcte
  timeout: 10000, // optionnel : délai d'expiration (en ms)
  headers: {
    'Content-Type': 'application/json',
  },
});



// Ajoute automatiquement le token d'auth si présent
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("refine-auth");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercepteur de réponse pour auto logout sur 401
api.interceptors.response.use(
  response => response,
  error => {
    // Timeout ou non autorisé
    if (
      error.code === "ECONNABORTED" ||
      error.response?.status === 401 ||
      error.response?.status === 403
    ) {
      // Nettoie le token/localStorage si besoin
      localStorage.removeItem("refine-auth");
      // Redirige vers login
      window.location.href = "/login";
      // Ou si tu utilises un navigate, fais navigate("/login");
    }
    return Promise.reject(error);
  }
);

export default api;
