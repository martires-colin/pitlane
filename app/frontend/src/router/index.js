import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import CreateAccount from "../views/CreateAccount.vue";
import Standings from "../views/Standings.vue";
import Schedule from "../views/Schedule.vue";
import Pitlane from "../views/Pitlane.vue";
import Home from "../views/Home.vue";
import Fantasy from "../views/Fantasy.vue";
import Settings from "../views/Settings.vue";

const routes = [
  {
    path: "/pitlane",
    name: "Pitlane",
    component: Pitlane,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/create-account",
    name: "CreateAccount",
    component: CreateAccount,
  },
  {
    path: "/standings",
    name: "Standings",
    component: Standings,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/schedule",
    name: "Schedule",
    component: Schedule,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/fantasy",
    name: "Fantasy",
    component: Fantasy,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
    meta: {
      requiresAuth: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
