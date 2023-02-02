// By Colin Martires

import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

//Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyB8fx4XTZBGanb2GzcAyiZDae-6cPe9Yfc",
  authDomain: "pitlane-ad39e.firebaseapp.com",
  projectId: "pitlane-ad39e",
  storageBucket: "pitlane-ad39e.appspot.com",
  messagingSenderId: "93872254351",
  appId: "1:93872254351:web:71ae889089a14d5a00affa",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Auth
const auth = getAuth(app);

export { app, auth };
