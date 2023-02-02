<template>
  <div class="pitlane-container flex flex-row bg-[#1b1b1b]">
    <div class="sidebar bg-[#222222] overflow-hidden">
      <div class="ml-2 flex flex-col justify-start">
        <div class="flex flex-row justify-start">
          <img
            class="pt-2"
            src="@/assets/PL.png"
            alt="website logo"
            width="40"
            height="40"
          />
          <h1 class="py-2 pl-[12px] text-2xl fw400">Pitlane</h1>
        </div>
        <div class="pt-4 flex flex-col">
          <SidebarLink to="/" icon="fas fa-home"> Home </SidebarLink>
          <SidebarLink to="/pitlane" icon="fa-solid fa-square-poll-vertical">
            Pitlane
          </SidebarLink>
          <SidebarLink to="/standings" icon="fa-solid fa-ranking-star">
            Standings
          </SidebarLink>
          <SidebarLink to="/schedule" icon="fa-solid fa-calendar-days">
            Schedule
          </SidebarLink>
          <SidebarLink v-if="user.loggedIn" to="/fantasy" icon="fa-solid fa-flag-checkered"
            >Fantasy
          </SidebarLink>
          <SidebarLink v-if="user.loggedIn" to="/settings" icon="fa-solid fa-gears">
            Settings
          </SidebarLink>
          <SidebarLink v-if="user.loggedIn" @click.prevent="signOut" to="/" icon="fa-solid fa-right-to-bracket">
            Logout
          </SidebarLink>
          <SidebarLink v-else  to="/login" icon="fa-solid fa-right-to-bracket">
            Login
          </SidebarLink>
        </div>
      </div>
      <!-- <Sidebar /> -->
      
    </div>
    <!-- <div :style="{ 'margin-left': sidebarWidth }"></div> -->
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
// import Sidebar from "./components/Sidebar";
import SidebarLink from "./components/SidebarLink.vue";



// import { sidebarWidth } from "./components/state";
export default {
  components: { SidebarLink },
  // setup() {
  //   return { sidebarWidth };
  // },
};
</script>

<script setup>
import { onMounted } from 'vue';
import { useStore } from 'vuex';
import { computed } from "vue";

const store = useStore();
onMounted(() => {
  store.dispatch("fetchUpcoming");
})

const user = computed(() => {
  return store.getters.user
})

const signOut = async () => {
  await store.dispatch("logout")
}

</script>

<style>
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  font-family: "Roboto Mono";
  text-align: center;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  /* background-color: #2c3e50; */
  max-width: none;
  width: 100%;
  color: white;
}

/* nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
} */

.pitlane-container {
  display: flex;
  flex-direction: row;
  min-height: 100vh;
  max-height: none;
  max-width: none;
}
.sidebar {
  width: 60px;
  transition: 0.4s ease;
}
.sidebar:hover {
  width: 170px;
}
.content {
  flex-grow: 1;
  /* text-align: center; */
}
</style>
