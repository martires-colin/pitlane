import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Standings from "../views/Standings.vue";
import Pitlane from "../views/Pitlane.vue";

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
    path: "/standings",
    name: "Standings",
    component: Standings,
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
