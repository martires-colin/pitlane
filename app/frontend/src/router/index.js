/* eslint-disable */

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
import League from "../components/League.vue"
import LeagueManage from "../components/LeagueManage.vue"
import FormLeague from "../components/FormLeague.vue"
import AdminConsole from "../views/AdminConsole.vue"

import store from "../store/index";


// try {
//   console.log(store)
//   console.log(store.getters.isAdmin)
// }
// catch(error) {
//   console.log(error)
// }

const routes = [
  {
    path: "/pitlane",
    name: "Pitlane",
    component: Pitlane,
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
  },
  {
    path: "/standings/:year",
    component: StandingsYear,
  },
  {
    path: "/schedule",
    name: "Schedule",
    component: Schedule,
  },
  {
    path: "/schedule/:year",
    component: ScheduleYear,
  },
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/fantasy",
    name: "Fantasy",
    component: Fantasy,
    meta: {
      requiresLogin: true,
    },
  },
  {
    path: "/fantasy/create",
    name: "CreateLeague",
    component: CreateLeague,
    meta: {
      requiresLogin: true,
    }
  },
  {
    path: "/fantasy/join",
    name: "JoinLeague",
    component: JoinLeague,
    meta: {
      requiresLogin: true,
    }
  },
  {
    path: "/fantasy/join/:inviteCode",
    component: JoinLeague,
  },
  {
    path: "/fantasy/manage",
    name: "Manage League",
    component: ManageLeagues,
    meta: {
      requiresLogin: true,
      requiresLeagueOwner: true,
    }
  },
  {
    path: "/fantasy/manage/:id",
    name: "Manage League ID",
    component: LeagueManage,
    meta: {
      requiresLogin: true,
      requiresLeagueOwner: true,
    },
    children: [
      { path: '', component: League },
      { path: 'edit/:tid', component: FormLeague }
    ]
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
    meta: {
      requiresLogin: true,
    },
  },
  {
    path: "/forgot-password",
    name: "ForgotPassword",
    component: ForgotPassword,
    meta: {
      requiresLogin: true,
    },
  },
  {
    path: "/admin-console",
    name: "Admin Console",
    component: AdminConsole,
    meta: {
      requiresLogin: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to) => {
  if (to.meta.requiresLeagueOwner && !store.getters.isLeagueOwner){
    return {name: 'CreateLeague'}
  }
  if (to.meta.requiresAuth && !store.getters.isAdmin) {
    return {name: 'Home'}
  }
  if (to.meta.requiresLogin && !store.getters.isLoggedIn) {
    return {name: 'Login'}
  }
})

export default router;
