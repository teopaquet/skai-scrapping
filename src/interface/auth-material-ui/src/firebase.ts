// firebase.ts
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// Add other imports (auth, firestore, etc.) as needed

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCksuRfxMX3jgKMHTfqHx6K6T7NpdK0YNU",
  authDomain: "skai-airline-data.firebaseapp.com",
  databaseURL: "https://skai-airline-data-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "skai-airline-data",
  storageBucket: "skai-airline-data.firebasestorage.app",
  messagingSenderId: "268681925960",
  appId: "1:268681925960:web:eb6b5e73575ee0d3cbcf7d"
};

// Initialize Firebase
export const firebaseApp = initializeApp(firebaseConfig);
