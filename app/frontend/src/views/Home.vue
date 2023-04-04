<!-- By Anthony Ganci and Colin Martires -->
<script>
// import Schedule from "../components/ScheduleComp";
// import Standings from "../components/StandingsComp";
// import axios from 'axios';
import { useStore} from "vuex";
import { useRouter } from "vue-router";
import {computed} from "vue";
import { auth } from '../firebase'
export default {
  // components: {Schedule, Standings},
  name: "Home",
  setup() {
    const store = useStore()
    const router = useRouter()

    auth.onAuthStateChanged(user => {
      // console.log("onAuthState")
      // console.log(user)
      store.dispatch("fetchUser", user)
    })
    const user = computed(() => {
      return store.getters.user
    })
    const signOut = async () => {
      await store.dispatch("logout")
      router.push('/')
    }
    return { user, signOut }
  },
  data() {
    return {
      username: "",
      userFeed: null,
    }
  },
  methods: {
    async fetchUserFeed() {
      // const res = await fetch('')
    }
  },
  //lifecycle hooks
  beforeUpdate() {
    const store = useStore()
    auth.onAuthStateChanged(user => {
      store.dispatch("fetchUser", user)
    })
    const user = computed(() => {
      return store.getters.user.displayName
    })

    this.username = user

    return { user }
  },
  mounted() {
    if (this.user.loggedIn) {
      // this.fetchUserFeed()
    }
  }
  

};
</script>

<!-- <script setup>
// import {ref, onMouted, computed} from 'vue
import { onMounted } from 'vue';
import { useStore } from 'vuex';
const store = useStore();
onMounted(() => {
  store.dispatch("fetchUpcoming");
})
</script> -->

<style scoped >
  @media(min-width: 2560px){
    .pitlane-landing {
      height: 600px;
      background-image: url('../assets/PITLANE.jpg');  
      /* // background-attachment: fixed; */
      background-repeat: no-repeat;
      background-size: cover;
      background-position: center 0px;
    }
  } 
  @media(min-width: 1025px) and (max-width: 2559px){
    .pitlane-landing {
      height: 500px;
      background-image: url('../assets/PITLANE.jpg');  
      /* // background-attachment: fixed; */
      background-repeat: no-repeat;
      background-size: cover;
      background-position: center 0px;
    }
  } 
  @media(min-width: 481px ) and (max-width: 1024px) {
    .pitlane-landing {
      height: 300px;
      background-image: url('../assets/PITLANE.jpg');  
      background-repeat: no-repeat;
      background-size: cover;
    }
  }
  @media (max-width: 480px) {
    .pitlane-landing {
      height: 200px;
      background-image: url('../assets/PITLANE.jpg');  
      background-repeat: no-repeat;
      background-size: cover;
    }
  }
  
</style>

<template>
  <div class="flex flex-col justify-center">
    <div class="pitlane-landing flex justify-center">
    </div>

    <div v-if="user.loggedIn">
      <p class="pt-3">Welcome, {{ user.displayName }}</p>
    </div>

    <div class="py-2 flex flex-row justify-evenly">
      <div class="previous-race">
        <p class="text-red-500 text-xl pb-2">Previous Race</p>
        <div class="flex flex-row">
          <img :src="$store.state.prevRace[3]" :alt="$store.state.prevRace[3]" class="h-[24px] w-[40px] border border-black"/>
          <p class="pl-4">{{ $store.state.prevRace[0] }} </p>
        </div>
        <p>{{ $store.state.prevRace[1] }} </p>
      </div>
      <div class="upcoming-race">
        <p class="text-green-500 text-xl pb-2">Upcoming Race</p>
        <div class="flex flex-row">
          <img :src="$store.state.nextRace[3]" :alt="$store.state.nextRace[3]" class="h-[24px] w-[40px] border border-black"/>
          <p class="pl-4"> {{ $store.state.nextRace[0] }}</p>
        </div>
        <p> {{ $store.state.nextRace[1] }}</p>
      </div>
    </div>
  </div>
  <div v-if="user.loggedIn" class="feed flex flex-col justify-center">
    <!-- Carousel. Retrieve images only problem is that this could take a while to load maybe.-->
  </div>
</template>