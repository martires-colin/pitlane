<template>
<div class="flex flex-col justify-center">
  <div class="pitlane-landing">
    <h1 class="py-2 text-4xl font-[500]">Pitlane</h1>
    <h2 class="opacity-50 font-[300] text-xl">Formula1 made simple.</h2>
  </div>
  
  <div v-if="user.loggedIn">
    <p class="pt-3">Welcome, {{user.data.displayName}}</p>
  </div>

  <div class="py-2 flex flex-row justify-evenly">
    <div class="previous-race">
      <p class="text-red-500 text-xl">Previous Race</p>
      <p>{{ $store.state.prevRace[0] }} </p>
      <p>{{ $store.state.prevRace[1] }} </p>
    </div>
    <div class="upcoming-race">
      <p class="text-green-500 text-xl">Upcoming Race</p>
      <p> {{ $store.state.nextRace[0] }}</p>
      <p> {{ $store.state.nextRace[1] }}</p>
    </div>
  </div>

</div>
<!-- <div class="landing">
  <div id="landing-1" >
    <Schedule/>
  </div>
  <div id="landing-2">
    <Standings/>
  </div>
</div> -->

</template>

<script>
// import Schedule from "../components/ScheduleComp";
// import Standings from "../components/StandingsComp";
// import axios from 'axios';
import { useStore} from "vuex";
import { useRouter } from "vue-router";
import {computed} from "vue";
import { auth } from '../firebase'

export default {
  name: "Home",
  setup() {
    const store = useStore()
    const router = useRouter()

    auth.onAuthStateChanged(user => {
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
// components: {Schedule, Standings},

  data() {
    return {
    }
  },
  methods: {
  },
  created() {
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

<style scoped lang="scss">
// h1 {
//   padding-top: 1rem;
// }
// .landing {
//   display: flex;
//   flex-direction: row;
//   font-family: "Roboto Mono";
// }
.pitlane-landing {
  height: 400px;
  background-image: url('../assets/pitwall-main.png');
  background-repeat: no-repeat;
  background-size: cover;
  background-position-y: -55px;
}

// #landing-1 {
//   padding-right: 5rem;
//   // max-height: 300px;
//   // overflow: auto;
// }
</style>