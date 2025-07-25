// firebase.ts
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore, collection, getDocs } from 'firebase/firestore/lite';
// Add other imports (auth, firestore, etc.) as needed

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCUua7RO6C4I0rfXPekgZKT8MXSeCBervg",
  authDomain: "skai-tech-visualizer.firebaseapp.com",
  databaseURL: "https://skai-tech-visualizer-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "skai-tech-visualizer",
  storageBucket: "skai-tech-visualizer.appspot.com",
  messagingSenderId: "869942181646",
  appId: "1:869942181646:web:596f8dba3384c13f5c215f"
};

// Initialize Firebase
export const firebaseApp = initializeApp(firebaseConfig);
