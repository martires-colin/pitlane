// import { createApp } from "vue";
import { createSSRApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Cleave from "vue-cleave-component";
import  BootstrapVue3  from "bootstrap-vue-3";
import "@fortawesome/fontawesome-free/js/all";
import "bootstrap/dist/css/bootstrap.css";
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';
import './styles/app.css';

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css' 


const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
  },
})

createSSRApp(App).use(router).use(store).use(vuetify).use(Cleave).use(BootstrapVue3).mount("#app");
