import { createRouter, createWebHistory } from "vue-router";
import Pitlane from "../components/Pitlane.vue";
import Login from "../views/Login.vue";
import Results from "../views/Results.vue";

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
    path: "/results",
    name: "Results",
    component: Results,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;