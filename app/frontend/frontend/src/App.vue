<template>
  <div>
    <Sidebar />
    <div :style="{ 'margin-left': sidebarWidth }"></div>

    <router-link to="/pitlane">Pitlane</router-link>
    <router-link to="/login">Login</router-link>
    <router-link to="/results">Results</router-link>
    <router-view />
  </div>
</template>

<script>
import Sidebar from "./components/Sidebar";
import { sidebarWidth } from "./components/state";
export default {
  components: { Sidebar },
  setup() {
    return { sidebarWidth };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
