<template>
  <v-app full-height theme="dark">
    <v-app-bar flat >
      <img src="@/assets/PL.png" class="d-inline-block align-top ml-2" alt="Pitlane" width="40"
            height="40">
      <p class="px-4 text-3xl">PITLANE</p>
      <v-container v-if="(windowWidth < 854)" class="pitlane-nav flex justify-end align-center py-0">
        <v-menu location="bottom">
          <template v-slot:activator="{ props }">
            <v-btn class=""
              v-bind="props"
              icon="mdi-menu"
            >
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              v-for="link in links"
              :key="link"
              @click="$router.push(link[1])">
              {{ link[0] }}
            </v-list-item>
            <v-menu location="left" v-if="$store.getters.isLoggedIn">
              <template v-slot:activator="{ props }">
                <v-list-item
                  v-bind="props"
                >
                  Fantasy
                </v-list-item>
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
            <v-list-item v-if="user.loggedIn" @click="$router.push('/admin-console')">
              Admin
            </v-list-item>
          </v-list>
        </v-menu>
        <v-menu location="bottom" v-if="$store.getters.isLoggedIn">
          <template v-slot:activator="{ props }">
            <v-avatar
              color="grey-darken-1"
              size="40"
              :image="user.photoURL"
              v-bind="props"
            ></v-avatar>
          </template>
          <v-list>
            <v-list-item @click="$router.push('/settings')">
              <v-list-item-title>Settings</v-list-item-title>
            </v-list-item>
            <v-list-item>
              <v-list-item-title @click="logout_dialog = true">Logout</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-menu location="bottom" v-if="!$store.getters.isLoggedIn">
          <template v-slot:activator="{ props }">
            <v-avatar
              color="grey-darken-1"
              size="40"
              v-bind="props"
            ></v-avatar>
          </template>
          <v-list>
            <v-list-item @click="$router.push('/login')">
              Login
            </v-list-item>
          </v-list>
        </v-menu>
      </v-container>
      <v-container v-else class="d-flex align-center mr-0 pitlane-nav">
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
            <!-- <v-btn v-if="user.loggedIn" variant="text" @click="$router.push('/settings')">
            Settings
            </v-btn>
            <v-btn v-if="user.loggedIn" variant="text" @click="logout_dialog = true">
            Logout
            </v-btn> -->
            <v-btn v-if="!user.loggedIn" variant="text" @click="$router.push('/login')">
              Login
            </v-btn> 

            <v-menu location="bottom" v-if="$store.getters.isLoggedIn">
              <template v-slot:activator="{ props }">
                <v-avatar
                  color="grey-darken-1"
                  size="40"
                  :image="user.photoURL"
                  v-if="user.loggedIn"
                  v-bind="props"
                ></v-avatar>
              </template>
              <v-list>
                <v-list-item v-if="user.loggedIn" @click="$router.push('/settings')">
                  <v-list-item-title>Settings</v-list-item-title>
                </v-list-item>
                <v-list-item v-if="user.loggedIn">
                  <v-list-item-title @click="logout_dialog = true">Logout</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>

            <!-- <v-avatar
              color="grey-darken-1"
              size="40"
              :image="user.photoURL"
              v-if="user.loggedIn"
            ></v-avatar> -->
          </div>

      </v-container>
    </v-app-bar>
    <v-main class="bg-[#36393e] pitlane-container">
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

const windowWidth = ref(window.innerWidth)

onMounted(() => {
  store.dispatch("fetchUpcoming");
  window.onresize = () => {
    windowWidth.value = window.innerWidth
  }
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

.pitlane-nav {

}


@media(min-width: 2560px){
    .pitlane-nav {
      height: 5vh;
    }
    .pitlane-container {
      height: 95vh;
    }
  } 
  @media(min-width: 1025px) and (max-width: 2559px){
    .pitlane-nav {
      height: 5vh;
    }
    .pitlane-container {
      height: 95vh;
    }
  } 
  @media(max-width: 865px) {
    .pitlane-nav {
      height: 6vh;
    }
    .pitlane-container {
      height: 94vh;
    }
    .pitlane-nav-menu {
      position: absolute;
      top: 5px;
      right: 5px;
    }
    
  }

</style>
