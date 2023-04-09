<template>
  <v-app full-height theme="dark">
    <v-app-bar flat class="h-[8vh]">
      <img src="@/assets/PL.png" class="d-inline-block align-top ml-2" alt="Pitlane" width="40"
            height="40">
      <p class="px-4 text-3xl">Pitlane</p>
      <v-container class="fill-height d-flex align-center mr-0">
        
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
                <v-list-item v-if="$store.state.user.roles.isLeagueOwner" @click="$router.push('/fantasy/manage')">
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

            <v-btn v-if="user.loggedIn && user.roles.isAdmin" variant="text" @click="$router.push('/admin-console')">
            Admin
            </v-btn>
            <v-btn v-if="user.loggedIn" variant="text" @click="$router.push('/settings')">
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
              color="grey-darken-1"
              size="40"
              :image="user.photoURL"
              v-if="user.loggedIn"
            ></v-avatar>
          </div>

      </v-container>
    </v-app-bar>
    <v-main class="bg-[#36393e] h-[92vh]">
      <v-container fluid class="p-0 h-full">
        <router-view/>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { onMounted, computed  } from 'vue';
import { useStore } from 'vuex';
// import { useRouter } from 'vue-router'
import SidebarLink from "./components/SidebarLink.vue";

const store = useStore();

onMounted(() => {
  store.dispatch("fetchUpcoming");
  // console.log('League owner?:', store.getters.isLeagueOwner)
  // console.log('League Owner User:', store.state.user.roles.isLeagueOwner)
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
