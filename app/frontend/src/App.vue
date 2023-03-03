<template>
  <div class="pitlane-container flex flex-row bg-white text-slate-900 dark:bg-slate-800">
    <div class="relative sidebar overflow-hidden border-r border-slate-500 border-solid" :class="{'w-[170px]': isActive, 'w-[60px]': !isActive}">
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
        <div class="pt-4 flex flex-col text-slate-700">
          <SidebarLink to="/" icon="fas fa-home">
            Home
          </SidebarLink>
          <SidebarLink to="/pitlane" icon="fa-solid fa-square-poll-vertical">
            Pitlane
          </SidebarLink>
          <SidebarLink to="/standings" icon="fa-solid fa-ranking-star">
            Standings
          </SidebarLink>
          <SidebarLink to="/schedule" icon="fa-solid fa-calendar-days">
            Schedule
          </SidebarLink>
          <!-- <div class="fantasyDrop text-start" @mouseover="fantasyDropdown = true" @mouseleave="fantasyDropdown = false"> -->
          <div v-if="user.loggedIn" class="fantasyDrop text-start">
            <SidebarLink class="fantasy-link" v-if="user.loggedIn" to="/fantasy" icon="fa-solid fa-flag-checkered" @mouseover="fantasyDropdown = true"
              >Fantasy
            </SidebarLink>
            <div class="Drop text-start pt-3 text-sm opacity-75" v-if="fantasyDropdown && user.loggedIn">
              <SidebarLink icon="fa-solid fa-plus" v-if="user.loggedIn" class="pb-2" to="/fantasy/createLeague">Create a League</SidebarLink>
              <SidebarLink icon="fa-solid fa-user-plus" v-if="user.loggedIn" class="py-3" to="/fantasy/joinLeague">Join a League</SidebarLink>
              <SidebarLink icon="fa-solid fa-warehouse" v-if="user.loggedIn" to="/fantasy">My Teams</SidebarLink>
            </div>
          </div>
          <SidebarLink v-if="user.loggedIn" to="/settings" icon="fa-solid fa-gears">
            Settings
          </SidebarLink>
          <SidebarLink v-if="user.loggedIn" @click.prevent="signOut" to="/" icon="fa-solid fa-right-to-bracket">
            Logout
          </SidebarLink>

          <SidebarLink v-else to="/login" icon="fa-solid fa-right-to-bracket">
            Login
          </SidebarLink>
        </div>
        <div class="absolute bottom-3 right-5">
          <div :class="{'rotate-180': !isActive}" @click="(isActive = !isActive)">
            <i class="fa-solid fa-angles-left" />
          </div>
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
  components: {
    SidebarLink
  },
  // setup() {
  //   return { sidebarWidth };
  // },
  data() {
    return {
      isActive: true,
      fantasyDropdown: false,
      button: ">"
    }
  }
};
</script>

<script setup>
import { onMounted, computed  } from 'vue';
import { useStore } from 'vuex';


const store = useStore();

onMounted(() => {
  store.dispatch("fetchUpcoming");
})

const user = computed(() => {
  return store.getters.user
})

const signOut = async () => {
  if(confirm("Are you sure you want to logout?")) {
    await store.dispatch("logout")
  }
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
  min-height: 100%;
  max-height: none;
  transition: 0.4s ease;
}
.sidebar:hover {
  /* width: 170px; */
}
.fantasy-link:hover {
  width: 180px;
}
.fantasyDrop {
  height: 26px;
  overflow: hidden;
  transition: 0.4s ease;
}
.fantasyDrop:hover{
  height: 160px;
}
.content {
  flex-grow: 1;
  /* text-align: center; */
}
</style>
