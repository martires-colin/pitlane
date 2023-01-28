//the code in this file was taken fron a Firebase Vue Integration Tutorial
//https://www.youtube.com/watch?v=Kc-FbPSdezg

import { createStore } from "vuex";
import router from "../router";
import { auth } from "../firebase";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
} from "firebase/auth";
import axios from "axios";

export default createStore({
  state: {
    // user: null,
    // for testing purposes of fantasy while firebase is still being done
    user: ["Anthony"],
    nextRace: [],
    prevRace: null,
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },
    CLEAR_USER(state) {
      state.user = null;
    },
    SET_UPCOMING(state, upcoming) {
      state.nextRace = upcoming.nextRace
      state.prevRace = upcoming.prevRace
    }
  },
  actions: {
    async login({ commit }, details) {
      const { email, password } = details;

      try {
        await signInWithEmailAndPassword(auth, email, password);
      } catch (error) {
        switch (error.code) {
          case "auth/user-not-found":
            alert("User not found");
            break;
          case "auth/wrong-password":
            alert("Wrong password");
            break;
          default:
            alert(error.message);
        }
        return;
      }

      commit("SET_USER", auth.currentUser);
      router.push("/pitlane");
    },
    async register({ commit }, details) {
      const { email, password } = details;

      try {
        await createUserWithEmailAndPassword(auth, email, password);
      } catch (error) {
        switch (error.code) {
          case "auth/email-already-in-use":
            alert("Email already in use");
            break;
          case "auth/invalid-email":
            alert("Invalid email");
            break;
          case "auth/operation-not-allowed":
            alert("Operation not allowed");
            break;
          case "auth/weak-password":
            alert("Weak password");
            break;
          default:
            alert("Something went wrong");
        }
        return;
      }

      commit("SET_USER", auth.currentUser);
      router.push("/pitlane");
    },
    async logout({ commit }) {
      await signOut(auth);
      commit("CLEAR_USER");
      router.push("/login");
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
    getUpcoming: (state) => {state.nextRace, state.prevRace }
  }
});
