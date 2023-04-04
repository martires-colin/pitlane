// By Colin Martires

import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getFunctions } from "firebase/functions";

require("dotenv").config();

//Firebase configuration
const firebaseConfig = {
//   apiKey: process.env.API_KEY,
//   authDomain: process.env.AUTH_DOMAIN,
//   projectId: process.env.PROJECT_ID,
//   storageBucket: process.env.STORAGE_BUCKET,
//   messagingSenderId: process.env.MESSAGING_SENDER_ID,
//   appId: process.env.APP_ID,
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

// Initialize Firestore
const db = getFirestore(app)

// Initialize Cloud Functions
const functions = getFunctions(app)

export { app, auth, db, functions };
