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
            <v-btn v-if="user.loggedIn" variant="text" @click="logout_dialog = true">
            Logout
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

    <!-- logout dialog -->
    <v-dialog v-model="logout_dialog" width="auto">
      <v-card>
        <v-card-text>
          Are you sure you want to logout?
        </v-card-text>
        <div class="d-flex justify-content-center">
          <v-card-actions>
            <v-btn color="blue" variant="outlined" @click="logout_dialog = false">No</v-btn>
            <v-btn color="blue" variant="tonal" @click="signOut(), logout_dialog = false, $router.push('/')">Yes, I'm sure</v-btn>
          </v-card-actions>
        </div>
      </v-card>
    </v-dialog>

  </v-app>


</template>

<script setup>
import { onMounted, computed, ref  } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

onMounted(() => {
  store.dispatch("fetchUpcoming");
  // console.log('League owner?:', store.getters.isLeagueOwner)
  // console.log('League Owner User:', store.state.user.roles.isLeagueOwner)
})


const user = computed(() => {
  return store.getters.user
})

const logout_dialog = ref(false)
const signOut = async () => {
  console.log("Logging out!")
  await store.dispatch("logout")
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
