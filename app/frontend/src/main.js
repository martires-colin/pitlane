import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Cleave from "vue-cleave-component";
import  BootstrapVue3  from "bootstrap-vue-3";
import "@fortawesome/fontawesome-free/js/all";
import "bootstrap/dist/css/bootstrap.css";
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';
import './styles/app.css';

createApp(App).use(router).use(store).use(Cleave).use(BootstrapVue3).mount("#app");
