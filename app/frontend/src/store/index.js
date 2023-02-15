// By Anthony Ganci and Colin Martires

/*References 
  https://www.youtube.com/watch?v=Kc-FbPSdezg
  https://blog.logrocket.com/authentication-vue-3-firebase/
*/

import { createStore } from "vuex";
import VuexPersistence from "vuex-persist";
import axios from "axios";
import { auth } from "../firebase";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  // updateEmail,
  updateProfile
} from "firebase/auth";
import { db } from "../firebase"
import {
  doc,
  setDoc,
  getDoc,
  updateDoc
} from "firebase/firestore";
// import { useRouter } from 'vue-router'


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
      photoURL: null
    },
    nextRace: [],
    prevRace: null,
  },
  mutations: {
    SET_LOGGED_IN(state, value) {
      state.user.loggedIn = value
    },
    SET_USER(state, data) {
      state.user.displayName = data.displayName
      state.user.email = data.email
      state.user.photoURL = data.photoURL
    },
    SET_USER_PHONENUMBER(state, data) {
      state.user.phoneNumber = data
    },
    SET_UPCOMING(state, upcoming) {
      state.nextRace = upcoming.nextRace
      state.prevRace = upcoming.prevRace
    }
  },
  actions: {
    async register({ commit }, { email, password, name}) {
      // const router = useRouter()
      const response = await createUserWithEmailAndPassword(auth, email, password)
      if (response) {
        updateProfile(response.user, {
          displayName: name,
          // temporary initial profile pic of Danny Ric
          photoURL: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSkcZ1uxSAfe3xexNQXU53iaD9jocSvJGAEIw&usqp=CAU",
        })
        commit('SET_USER', response.user)
        // db.collection('users').doc(response.user.uid).set({
        //   phoneNumber: "",
        //   username: name
        // })
        try {
          await setDoc(doc(db, "users", response.user.uid), {
            username: name,
            email: email,
            password: password,
            phoneNumber: ""
          });
          console.log("Document written with ID: ", response.user.uid);
        } catch (e) {
          console.error("Error adding document: ", e);
        }
        console.log(response.user)
        // router.push("/")
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
        } else {
          console.log("No such document")
        }
        commit('SET_USER', response.user)
        // commit('SET_USER', { phoneNumber: user.phoneNumber})
      } else {
        throw new Error('Login Failed')
      }
    },
    async updatePhoneNumber({ commit }, { phoneNumber }) {
      const user = auth.currentUser;
      const docRef = doc(db, "users", user.uid)
      await updateDoc(docRef, {
        phoneNumber: phoneNumber
      })
      commit('SET_USER_PHONENUMBER', phoneNumber)
    },
    async logout({ commit }) {
      await signOut(auth)
      commit('SET_USER', {
        loggedIn: false,
        displayName: null,
        email: null,
        phoneNumber: null,
        photoURL: null
      })
    },
    async fetchUser({ commit }, user) {
      commit('SET_LOGGED_IN', user !== null)
      if (user) {
        commit('SET_USER', {
          displayName: user.displayName,
          email: user.email,
          phoneNumber: user.phoneNumber,
          photoURL: user.photoURL
        })
      } else {
        commit('SET_USER', {
          loggedIn: false,
          displayName: null,
          email: null,
          phoneNumber: null,
          photoURL: null
        })
      }
    },
    async fetchUpcoming({ commit }) {
      try {
        const payload = {
          Offseason: 'true',
        }
        const path = "http://localhost:3001/schedule/nextprev";
        await axios.post(path ,payload).then((response) => {
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
    getUpcoming: (state) => {state.nextRace, state.prevRace }
  },
  plugins: [vuexLocal.plugin]
});
