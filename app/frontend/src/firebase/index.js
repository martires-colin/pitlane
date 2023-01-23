//the code in this file was taken from a Firebase Vue Integration Tutorial
//https://www.youtube.com/watch?v=Kc-FbPSdezg

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
const auth = getAuth(app);

export { auth };
