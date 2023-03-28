<template>
  <!-- <div class="pitlane-container flex flex-row bg-white text-slate-900 dark:bg-slate-800"> -->
    <!-- <div class="navbar">
      <b-navbar variant="faded">
        <b-navbar-brand href="/">
          <img src="@/assets/PL.png" class="d-inline-block align-top" alt="Pitlane" width="40"
            height="40">
          Pitlane
        </b-navbar-brand>
        <b-navbar-nav class="ml-auto">
          <b-nav-item right href="/">Home</b-nav-item>

          <b-nav-item-dropdown text="Fantasy" right>
            <b-dropdown-item href="/fantasy">My Teams</b-dropdown-item>
            <b-dropdown-item href="/fantasy/createLeague">Create a League</b-dropdown-item>
            <b-dropdown-item href="/fantasy/joinLeague">Join a League</b-dropdown-item>
          </b-nav-item-dropdown>

          <b-nav-item-dropdown text="User" right>
            <b-dropdown-item href="#">Account</b-dropdown-item>
            <b-dropdown-item href="#">Settings</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-navbar>
    </div> -->
  <div>
    <b-navbar toggleable="lg" dark="true" variant="dark">
      <b-navbar-brand href="/">
        <img src="@/assets/PL.png" class="d-inline-block align-top" alt="Pitlane" width="40"
          height="40">
        Pitlane
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">

          <b-nav-item href="/">Home</b-nav-item>
          <b-nav-item href="/pitlane">Pitlane</b-nav-item>
          <b-nav-item href="/standings">Standings</b-nav-item>
          <b-nav-item href="/schedule">Schedule</b-nav-item>
          <b-nav-item-dropdown text="Fantasy" v-if="user.loggedIn">
            <b-dropdown-item href="/fantasy">My Teams</b-dropdown-item>
            <b-dropdown-item href="/fantasy/createLeague">Create a League</b-dropdown-item>
            <b-dropdown-item href="/fantasy/joinLeague">Join a League</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item href="/settings" v-if="user.loggedIn">Settings</b-nav-item>
          <b-nav-item href="/" v-if="user.loggedIn" @click.prevent="signOut">Logout</b-nav-item>
          <b-nav-item href="/login" v-if="!user.loggedIn">Login</b-nav-item>

        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
  <div class="pitlane-container flex flex-row bg-[#36393e]">
    <!-- <div class="relative sidebar overflow-hidden" :class="{'w-[190px]': isActive, 'w-[58px]': !isActive}">
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
        <div class="pt-4 flex flex-col text-white">
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
          <div v-if="user.loggedIn" class="fantasyDrop text-start">
            <SidebarLink class="fantasy-link" v-if="user.loggedIn" to="/fantasy" icon="fa-solid fa-flag-checkered" @mouseover="fantasyDropdown = true"
              >Fantasy
            </SidebarLink>
            <div class="Drop text-start pt-3 text-sm opacity-75" v-if="fantasyDropdown && user.loggedIn && isActive">
              <SidebarLink icon="fa-solid fa-plus" v-if="user.loggedIn" class="pb-2" to="/fantasy/createLeague">Create a League</SidebarLink>
              <SidebarLink icon="fa-solid fa-user-plus" v-if="user.loggedIn" class="py-3" to="/fantasy/joinLeague">Join a League</SidebarLink>
              <SidebarLink icon="fa-solid fa-warehouse" v-if="user.loggedIn" to="/fantasy">My Teams</SidebarLink>
            </div>
            <div class="Drop text-start pt-3 text-sm opacity-75" v-if="fantasyDropdown && user.loggedIn && !isActive">
              <SidebarLink icon="fa-solid fa-plus" class="" to="/fantasy/createLeague"></SidebarLink>
              <SidebarLink icon="fa-solid fa-user-plus" class="py-3" to="/fantasy/joinLeague"></SidebarLink>
              <SidebarLink icon="fa-solid fa-warehouse" to="/fantasy"></SidebarLink>
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
      
    </div> -->
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<!-- <script>
// import Sidebar from "./components/Sidebar";
// import SidebarLink from "./components/SidebarLink.vue";
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
</script> -->

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
  /* background-color: #282b30; */
}
.sidebar:hover {
  /* width: 170px; */
}
.fantasy-link:hover {
  /* width: 180px; */
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
