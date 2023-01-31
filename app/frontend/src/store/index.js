// By Anthony Ganci and Colin Martires

import { createStore } from "vuex";
// import router from "../router";
import axios from "axios";
import { auth } from "../firebase";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  updateProfile
} from "firebase/auth";

export default createStore({
  state: {
    user: {
      loggedIn: false,  // tell whether user is logged in or not
      data: null  // data holds information about user
    },
    nextRace: [],
    prevRace: [],
  },
  mutations: {
    // SET_USER(state, user) {
    //   state.user = user;
    // },
    // CLEAR_USER(state) {
    //   state.user = null;
    // },
    SET_LOGGED_IN(state, value) {
      state.user.loggedIn = value
    },
    SET_USER(state, data) {
      state.user.data = data
    },
    SET_UPCOMING(state, upcoming) {
      state.nextRace = upcoming.nextRace
      state.prevRace = upcoming.prevRace
    }
  },
  actions: {
    // async login({ commit }, details) {
    //   const { email, password } = details;

    //   try {
    //     await signInWithEmailAndPassword(auth, email, password);
    //   } catch (error) {
    //     switch (error.code) {
    //       case "auth/user-not-found":
    //         alert("User not found");
    //         break;
    //       case "auth/wrong-password":
    //         alert("Wrong password");
    //         break;
    //       default:
    //         alert(error.message);
    //     }
    //     return;
    //   }

    //   commit("SET_USER", auth.currentUser);
    //   router.push("/pitlane");
    // },
    // async register({ commit }, details) {
    //   const { email, password } = details;

    //   try {
    //     await createUserWithEmailAndPassword(auth, email, password);
    //   } catch (error) {
    //     switch (error.code) {
    //       case "auth/email-already-in-use":
    //         alert("Email already in use");
    //         break;
    //       case "auth/invalid-email":
    //         alert("Invalid email");
    //         break;
    //       case "auth/operation-not-allowed":
    //         alert("Operation not allowed");
    //         break;
    //       case "auth/weak-password":
    //         alert("Weak password");
    //         break;
    //       default:
    //         alert("Something went wrong");
    //     }
    //     return;
    //   }

    //   commit("SET_USER", auth.currentUser);
    //   router.push("/pitlane");
    // },
    // async logout({ commit }) {
    //   await signOut(auth);
    //   commit("CLEAR_USER");
    //   router.push("/login");
    // },

    async register({ commit }, { email, password, name}) {
      const response = await createUserWithEmailAndPassword(auth, email, password)
      if (response) {
        console.log(response)
        commit('SET_USER', response.user)
        // response.user.updateProfile({displayName: name})
        updateProfile(response.user, {
          displayName: name
        })
        console.log(response)
      } else {
        throw new Error("Unable to register user")
      }

      // try {
      //   const { user } = await createUserWithEmailAndPassword(auth, email, password);
      // } catch (error) {
      //   switch (error.code) {
      //     case "auth/email-already-in-use":
      //       alert("Email already in use");
      //       break;
      //     case "auth/invalid-email":
      //       alert("Invalid email");
      //       break;
      //     case "auth/operation-not-allowed":
      //       alert("Operation not allowed");
      //       break;
      //     case "auth/weak-password":
      //       alert("Weak password");
      //       break;
      //     default:
      //       alert("Something went wrong");
      //   }
      //   return;
      // }

      // commit('SET_USER', user)
      // await updateProfile(user, {
      //   displayName: name
      // })
    },
    async login({ commit }, { email, password }) {
      const response = await signInWithEmailAndPassword(auth, email, password)
      if (response) {
        commit('SET_USER', response.user)
      } else {
        throw new Error('Login Failed')
      }
    },
    async logout({ commit }) {
      await signOut(auth)
      commit('SET_USER', null)
    },
    async fetchUser({ commit }, user) {
      commit('SET_LOGGED_IN', user !== null)
      if (user) {
        commit('SET_USER', {
          displayName: user.displayName,
          email: user.email
        })
      } else {
        commit('SET_USER', null)
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
  }
});
