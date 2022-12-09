import { createRouter, createWebHistory } from "vue-router";
import Pitlane from "../components/Pitlane.vue";

const routes = [
  {
    path: "/pitlane",
    name: "Pitlane",
    component: Pitlane,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
