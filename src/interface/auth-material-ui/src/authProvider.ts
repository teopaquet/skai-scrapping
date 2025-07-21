// import type { AuthProvider } from "@refinedev/core";
// import { apiService, TOKEN_KEY } from "./services/apiService";

// export { TOKEN_KEY } from "./services/apiService";

// export const authProvider: AuthProvider = {
//   login: async ({ username, email, password }) => {
//     try {
//       if ((username || email) && password) {
//         const data = await apiService.login({ username, email, password });

//         // Store the token in localStorage
//         localStorage.setItem(TOKEN_KEY, data.access_token);

//         return {
//           success: true,
//           redirectTo: "/",
//         };
//       }

//       return {
//         success: false,
//         error: {
//           name: "LoginError",
//           message: "Invalid username or password",
//         },
//       };
//     } catch (error: any) {
//       console.error("Login failed:", error);
//       return {
//         success: false,
//         error: {
//           name: "LoginError",
//           message: error.response?.data?.error_description || "Login failed",
//         },
//       };
//     }
//   },
//   logout: async () => {
//     localStorage.removeItem(TOKEN_KEY);
//     localStorage.removeItem("user"); // Clear user data if stored
//     return {
//       success: true,
//       redirectTo: "/login",
//     };
//   },
//   check: async () => {
//     const token = localStorage.getItem(TOKEN_KEY);
//     if (token) {
//       return {
//         authenticated: true,
//       };
//     }

//     return {
//       authenticated: false,
//       redirectTo: "/login",
//     };
//   },
//   getPermissions: async () => null,
//   getIdentity: async () => {
//     const token = localStorage.getItem(TOKEN_KEY);
//     if (!token) {
//       return null;
//     }

//     try {
//       return await apiService.getUserIdentity();
//     } catch (error: any) {
//       if (error.response?.status === 404) {
//         console.error("User identity endpoint not found:", error);
//         return null; // Return null or fallback logic
//       }
//       throw error; // Re-throw other errors
//     }
//   },
//   onError: async (error) => {
//     console.error(error);
//     return { error };
//   },
// };
