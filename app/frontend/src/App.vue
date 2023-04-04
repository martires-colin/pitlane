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
  <v-app full-height theme="dark">
    <v-app-bar flat height="80">
      <img src="@/assets/PL.png" class="d-inline-block align-top ml-2" alt="Pitlane" width="40"
            height="40">
      <p class=" px-4 text-3xl">Pitlane</p>
      <v-container class="fill-height d-flex align-center">
        
        <div class="ml-auto">
          <v-btn variant="text"
            v-for="link in links"
            :key="link"
            @click="$router.push(link[1])">
            {{ link[0] }}
            </v-btn>

            <v-menu location="bottom" v-if="$store.getters.isLoggedIn">
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                >
                  Fantasy
                </v-btn>
              </template>
              <v-list>
                <v-list-item v-if="$store.getters.isLeagueOwner" @click="$router.push('/fantasy/manage')">
                  <v-list-item-title>Manage Leagues</v-list-item-title>
                </v-list-item>

                <v-list-item
                  v-for="(item, index) in fantasyLinks"
                  :key="index"
                  :value="index"
                  @click="$router.push(item[1])"
                >
                  <v-list-item-title>{{ item[0] }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>

            <v-btn variant="text" @click="$router.push('/settings')">
            Settings
            </v-btn>
            <v-btn v-if="user.loggedIn" variant="text">
              <SidebarLink v-if="user.loggedIn" @click.prevent="signOut" to="/">
                Logout
              </SidebarLink>
            </v-btn>
            <v-btn v-else variant="text" @click="$router.push('/login')">
            Login
            </v-btn>

            <v-avatar
              class="me-10 ms-4"
              color="grey-darken-1"
              size="48"
              :image="user.photoURL"
            ></v-avatar>
        </div>

      </v-container>
    </v-app-bar>
    <v-main class="bg-[#36393e]">
      <v-container fluid class="p-0">
        <router-view/>
      </v-container>
    </v-main>
  </v-app>
  <!-- <div>
    <b-navbar toggleable="lg" dark="true" variant="dark">
      <b-navbar-brand href="/">
        <img src="@/assets/PL.png" class="d-inline-block align-top" alt="Pitlane" width="40"
          height="40">
        Pitlane
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">

          <b-nav-item href="/">Home</b-nav-item>
          <b-nav-item href="/pitlane">Pitlane</b-nav-item>
          <b-nav-item href="/standings">Standings</b-nav-item>
          <b-nav-item href="/schedule">Schedule</b-nav-item>
          <b-nav-item-dropdown text="Fantasy" v-if="user.loggedIn">
            <b-dropdown-item href="/fantasy">My Teams</b-dropdown-item>
            <b-dropdown-item href="/fantasy/manageLeagues" v-if="user.roles.leagueOwner">Manage Leagues</b-dropdown-item>
            <b-dropdown-item href="/fantasy/createLeague">Create a League</b-dropdown-item>
            <b-dropdown-item href="/fantasy/joinLeague">Join a League</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item href="/settings" v-if="user.loggedIn">Settings</b-nav-item>
          <b-nav-item href="/" v-if="user.loggedIn" @click.prevent="signOut">Logout</b-nav-item>
          <b-nav-item href="/login" v-if="!user.loggedIn">Login</b-nav-item>

        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div> -->
  <!-- <div class="pitlane-container flex flex-row bg-[#36393e]">

    <div class="content">
      
    </div>
  </div> -->
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
// import { useRouter } from 'vue-router'
import SidebarLink from "./components/SidebarLink.vue";

const store = useStore();

onMounted(() => {
  store.dispatch("fetchUpcoming");
  console.log('League owner?:', store.getters.isLeagueOwner)
})

const user = computed(() => {
  return store.getters.user
})

const signOut = async () => {
  if(confirm("Are you sure you want to logout?")) {
    // const router = useRouter()
    // router.push('/')
    await store.dispatch("logout")
  }
}

const links = [
  ['Home', '/'],
  ['Pitlane', '/pitlane'],
  ['Standings', '/standings'],
  ['Schedule', '/schedule']
]

const fantasyLinks = [
  ['My Teams', '/fantasy'],
  ['Create a League', '/fantasy/create'],
  ['Join a League', '/fantasy/join']
]

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
</style>
