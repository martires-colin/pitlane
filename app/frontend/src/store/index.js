// By Anthony Ganci and Colin Martires

import { createStore } from "vuex";
import VuexPersistence from "vuex-persist";
import axios from "axios";
import { auth, db } from "../firebase";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  updateProfile
} from "firebase/auth";
import {
  doc,
  setDoc,
  getDoc,
  updateDoc
} from "firebase/firestore";


const vuexLocal = new VuexPersistence({
  storage: window.localStorage
})

export default createStore({
  state: {
    user: {
      loggedIn: false,
      displayName: null,
      email: null,
      phoneNumber: null,
      photoURL: null,
      uid: null,
      notificationPreferences: {
        lightsOutNotif: false,
        upcomingRacesNotif: false,
        completeNotif: false,
        driverStandingsNotif: false,
        constructorStandingsNotif: false
      },
      roles: {
        isLeagueOwner: false,
        isTeamOwner: false,
        isAdmin: false, 
      }
    },
    nextRace: null,
    prevRace: null,
    userFeed: null, 
  },
  mutations: {
    SET_LOGGED_IN(state, value) {
      state.user.loggedIn = value
    },
    SET_USER(state, data) {
      state.user.displayName = data.displayName
      state.user.email = data.email
      state.user.photoURL = data.photoURL
      state.user.uid = data.uid
    },
    SET_USER_PHONENUMBER(state, value) {
      state.user.phoneNumber = value
    },
    SET_UPCOMING(state, upcoming) {
      state.nextRace = upcoming.nextRace
      state.prevRace = upcoming.prevRace
    },
    SET_NOTIFICATION_PREFERENCES(state, data) {
      state.user.notificationPreferences.lightsOutNotif = data.lightsOutNotif
      state.user.notificationPreferences.upcomingRacesNotif = data.upcomingRacesNotif
      state.user.notificationPreferences.completeNotif = data.completeNotif
      state.user.notificationPreferences.driverStandingsNotif = data.driverStandingsNotif
      state.user.notificationPreferences.constructorStandingsNotif = data.constructorStandingsNotif
    },
    SET_ROLES(state, data) {
      state.user.roles.isLeagueOwner = data.isLeagueOwner
    },
    SET_ADMIN_ROLE(state, data) {
      state.user.roles.isAdmin = data
    }
  },
  actions: {
    async register({ commit }, { email, password, name}) {
      const response = await createUserWithEmailAndPassword(auth, email, password)
      if (response) {
        updateProfile(response.user, {
          displayName: name,
          photoURL: "https://cdn-icons-png.flaticon.com/512/2266/2266048.png",
        })
        try {
          await setDoc(doc(db, "users", response.user.uid), {
            displayName: name,
            email: email,
            phoneNumber: "",
            uid: response.user.uid,
            photoURL: "https://cdn-icons-png.flaticon.com/512/2266/2266048.png"
          });
          console.log("Document written with ID: ", response.user.uid);
          await new Promise(r => setTimeout(r, 500));
        } catch (e) {
          console.error("Error adding document: ", e);
        }
        commit('SET_USER', response.user)
        console.log(response.user)
      } else {
        throw new Error("Unable to register user")
      }
    },
    async login({ commit }, { email, password }) {
      const response = await signInWithEmailAndPassword(auth, email, password)
      console.log(response)
      if (response) {
        const docRef = doc(db, "users", response.user.uid)
        const docSnap = await getDoc(docRef)
        if (docSnap.exists()) {
          console.log("Document data:", docSnap.data());
          commit('SET_USER_PHONENUMBER', docSnap.data().phoneNumber)
          commit('SET_ROLES', docSnap.data())
          commit('SET_ADMIN_ROLE', docSnap.data())
        } else {
          console.log("No such document")
        }
        commit('SET_USER', response.user)
      } else {
        throw new Error('Login Failed')
      }

      const user = auth.currentUser
      user.getIdTokenResult().then(idTokenResult => {
        console.log(idTokenResult.claims)
        commit('SET_ADMIN_ROLE', idTokenResult.claims.admin)
        const docRef = doc(db, "users", user.uid)
        updateDoc(docRef, {
          isAdmin: idTokenResult.claims.admin
        })
      })

    },
    async updatePhoneNumber({ commit }, { phoneNumber }) {
      const user = auth.currentUser;
      const docRef = doc(db, "users", user.uid)
      await updateDoc(docRef, {
        phoneNumber: phoneNumber
      })
      commit('SET_USER_PHONENUMBER', phoneNumber)
    },
    async updateNotifications({ commit }, notifPreferences) {
      const user = auth.currentUser;
      const docRef = doc(db, "users", user.uid)
      await updateDoc(docRef, {
        lightsOutNotif: notifPreferences.lightsOutNotif,
        upcomingRacesNotif: notifPreferences.upcomingRacesNotif,
        completeNotif: notifPreferences.completeNotif,
        driverStandingsNotif: notifPreferences.driverStandingsNotif,
        constructorStandingsNotif: notifPreferences.constructorStandingsNotif
      })
      commit('SET_NOTIFICATION_PREFERENCES', {
        lightsOutNotif: notifPreferences.lightsOutNotif,
        upcomingRacesNotif: notifPreferences.upcomingRacesNotif,
        completeNotif: notifPreferences.completeNotif,
        driverStandingsNotif: notifPreferences.driverStandingsNotif,
        constructorStandingsNotif: notifPreferences.constructorStandingsNotif
      })
    },
    async updateRoles({ commit }, userRoles) {
      const user = auth.currentUser;
      const docRef = doc(db, "users", user.uid)
      await updateDoc(docRef, {
        isLeagueOwner: userRoles.isLeagueOwner
      })
      commit('SET_ROLES', {
        isLeagueOwner: userRoles.isLeagueOwner
      })
    },
    async updateAdminRole({ commit }) {
      commit('SET_ADMIN_ROLE', true)
    },
    async updateProfilePicture({ commit }, img_url) {
      const user = auth.currentUser;
      await updateProfile(user, {
        photoURL: img_url.photoURL
      }).then(() => {
        const docRef = doc(db, "users", user.uid)
        updateDoc(docRef, {
          photoURL: img_url.photoURL
        })
        commit('SET_USER', {
          displayName: user.displayName,
          email: user.email,
          photoURL: user.photoURL,
          uid: user.uid
        })
      })
    },
    async updateUsername({ commit }, new_displayName) {
      const user = auth.currentUser;
      await updateProfile(user, {
        displayName: new_displayName
      }).then(() => {
        const docRef = doc(db, "users", user.uid)
        updateDoc(docRef, {
          displayName: new_displayName
        })
        commit('SET_USER', {
          displayName: user.displayName,
          email: user.email,
          photoURL: user.photoURL,
          uid: user.uid
        })
      })
    },
    async logout({ commit }) {
      await signOut(auth)
      commit('SET_USER', {
        loggedIn: false,
        displayName: null,
        email: null,
        photoURL: null
      })
      commit('SET_USER_PHONENUMBER', null)
      window.localStorage.clear()
    },
    async fetchUser({ commit }, user) {
      commit('SET_LOGGED_IN', user !== null)
      if (user) {
        commit('SET_USER', {
          displayName: user.displayName,
          email: user.email,
          photoURL: user.photoURL,
          uid: user.uid
        })
        const docRef = doc(db, "users", user.uid)
        const docSnap = await getDoc(docRef)
        if (docSnap.exists()) {
          console.log("Document data:", docSnap.data());
          commit('SET_USER_PHONENUMBER', docSnap.data().phoneNumber)
          commit('SET_ROLES', docSnap.data())
        } else {
          console.log("No such document")
        }
      } else {
        commit('SET_USER', {
          loggedIn: false,
          displayName: null,
          email: null,
          photoURL: null,
          uid: null
        })
        commit('SET_USER_PHONENUMBER', null)
      }
    },
    async fetchUpcoming({ commit }) {
      try {
        const path = "http://localhost:3001/schedule/nextprev";
        await axios.get(path).then((response) => {
          commit('SET_UPCOMING', response.data);
        })
      } catch (error) {
        alert(error);
        console.log(error);
      }
    },
  },
  getters: {
    user(state){
      return state.user
    },
    isLoggedIn(state){
      return state.user.loggedIn
    },
    isAdmin(state){
      return state.user.roles.isAdmin
      // return true
    },
    isLeagueOwner(state){
      return state.user.roles.isleagueOwner
      // return true
    },
    getUpcoming: (state) => {state.nextRace, state.prevRace }
  },
  plugins: [vuexLocal.plugin]
});
