import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
// import VueTelInput from "vue-tel-input";
import Cleave from "vue-cleave-component";
import  BootstrapVue3  from "bootstrap-vue-3";
import "@fortawesome/fontawesome-free/js/all";
import "bootstrap/dist/css/bootstrap.css";
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';
import './styles/app.css';
import 'vue-tel-input/dist/vue-tel-input.css';

createApp(App).use(router).use(store).use(Cleave).use(BootstrapVue3).mount("#app");
