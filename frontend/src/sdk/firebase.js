// Firebase JS SDK integration for email/password authentication
import { initializeApp } from "firebase/app";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";

console.log('Loaded API KEY:', process.env.REACT_APP_FIREBASE_API_KEY);

// Load Firebase config from environment variables
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Create user with email and password
export async function registerWithEmail(email, password) {
  return createUserWithEmailAndPassword(auth, email, password);
}

// Sign in with email and password
export async function loginWithEmail(email, password) {
  return signInWithEmailAndPassword(auth, email, password);
}

export { auth };
