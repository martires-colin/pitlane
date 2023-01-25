<script>
// import Schedule from "../components/ScheduleComp";
// import Standings from "../components/StandingsComp";
// import axios from 'axios';
export default {
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

<template>
  <Suspense>
    
  </Suspense>
  <div class="flex flex-col justify-center">
    <div class="pitlane-landing">
      <h1 class="py-2 text-4xl font-[500]">Pitlane</h1>
      <h2 class="opacity-50 font-[300] text-xl">Formula1 made simple.</h2>
    </div>
    <div class="py-2 flex flex-row justify-evenly">
      <div class="previous-race">
        <p class="text-red-500 text-xl pb-2">Previous Race</p>
        <div class="flex flex-row">
          <img v-if="$store.state.prevRace != null" :src="$store.state.prevRace[2]" alt="" height="40" width="40"/>
          <p class="pl-4">{{ $store.state.prevRace[0] }} </p>
        </div>
        <p>{{ $store.state.prevRace[1] }} </p>
      </div>
      <div class="upcoming-race">
        <p class="text-green-500 text-xl pb-2">Upcoming Race</p>
        <div class="flex flex-row">
          <img :src="$store.state.nextRace[2]" alt="" height="40" width="40"/>
          <p class="pl-4"> {{ $store.state.nextRace[0] }}</p>
        </div>
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