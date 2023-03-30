import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import CreateAccount from "../views/CreateAccount.vue";
import Standings from "../views/Standings.vue";
import Schedule from "../views/Schedule.vue";
import Pitlane from "../views/Pitlane.vue";
import Home from "../views/Home.vue";
import Fantasy from "../views/Fantasy.vue";
import Settings from "../views/Settings.vue";
import ScheduleYear from "../views/ScheduleYear.vue"
import StandingsYear from "../views/StandingsYear.vue"
import CreateLeague from "../views/CreateLeague.vue"
import JoinLeague from "../views/JoinLeague.vue"
import ForgotPassword from "../views/ForgotPassword.vue"
import ManageLeagues from "../views/ManageLeagues.vue"

// const Year = {
//   template: '<div> YEAR: {{ $route.params.year }}</div>'
// }

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
    path: "/standings/:year",
    component: StandingsYear,
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
    path: "/schedule/:year",
    component: ScheduleYear,
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
    path: "/fantasy/createLeague",
    name: "CreateLeague",
    component: CreateLeague,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: "/fantasy/joinLeague",
    name: "JoinLeague",
    component: JoinLeague,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: "/fantasy/joinLeague/:inviteCode",
    component: JoinLeague,
  },
  {
    path: "/fantasy/manageLeagues",
    name: "Manage League",
    component: ManageLeagues,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/forgot-password",
    name: "ForgotPassword",
    component: ForgotPassword,
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
