<!-- Started by Anthony Ganci -->

<template>
  <div v-if="ready" class="flex flex-col h-screen">
    <div class="flex flex-row justify-between p-4">
      <h1>{{ $store.state.user[0]}}'s Fantasy League</h1>
      <h1>Total points: 0</h1>
    </div>
    <div class="flex flex-row justify-evenly px-10 pb-2">
      <div class="flex flex-row">
          <p class="text-red-500 pr-4">Previous Race</p>
          <img :src="$store.state.prevRace[2]" alt="" height="40" width="40"/>
          <p class="px-4">{{ $store.state.prevRace[0] }} </p>
          <p>{{ $store.state.prevRace[1] }} </p>
      </div>
      <div class="flex flex-row">
          <p class="text-green-500 pr-4">Next Race</p>
          <img :src="$store.state.nextRace[2]" alt="" height="40" width="40"/>
          <p class="px-4"> {{ $store.state.nextRace[0] }}</p>
          <p>{{ $store.state.nextRace[1] }} </p>
      </div>
    </div>
    <div class="fantasy-grid">
      <div class="bg-dark-300 flex flex-col justify-evenly">
        <div class="flex flex-row justify-evenly">
          <div class="driver-item">
            <p v-if="driver1 === ''" class="py-2">Add Driver</p>
            <FantasyModal buttonTitle="+" :allDrivers="allDrivers" @set-Driver1="setDriver1" v-if="driver1 === ''" />
            <p class="pt-28 text-xl" v-if="driver1 !== ''">{{ driver1 }}</p>
            <FantasyModal buttonTitle="Edit" :allDrivers="allDrivers" @set-Driver1="setDriver1" v-if="driver1 !== ''" />
          </div>
          <div class="driver-item">
            <p class="py-2">Add Driver</p>
            <p class="pt-[60px] text-xl">+</p>
          </div>
        </div>
        <div class="flex flex-row justify-center">
          <div class="bg-slate-500 h-32 w-50 rounded-[20px]">
            <p class="py-2">Add Constructor</p>
            <p class="pt-4 text-xl">+</p>
          </div>
        </div>
      </div>
      <div class="bg-dark-300">
        <div class="bg-clip-content team-grid bg-jelly-bean-500">
          <div class="grid-item bg-jelly-bean-900 border-x-2 border-t-2 border-jelly-bean-600">Drivers</div>
          <div class="grid-item bg-jelly-bean-800 border-t-2 border-r-2 border-jelly-bean-600">Constructors</div>
          <div class="grid-item col-span-2 border-x-2 border-t-2 border-jelly-bean-600" v-for="(constructor, index) in allConstructors" :key="index">{{ constructor }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FantasyModal from "../components/FantasyModal.vue";

export default {
  components: {
    FantasyModal
  },
  data() {
    return {
      allDrivers: null,
      allConstructors: null,
      ready: false,
      driver1: "",
      driver2: "",
    }
  },
  methods: {
    setDriver1(str) {
      console.log(str)
      this.driver1 = str;
      // console.log(this.allDrivers)
      // this.allDrivers.splice(this.allDrivers.indexOf(str), 1);
      // console.log(this.allDrivers)
    },
    async fetchDrivers() {
      const res = await fetch(`http://localhost:3001/fantasy/drivers`);
      const data = await res.json();
      console.log(data)
      this.allDrivers = data.drivers;
    },
    async fetchConstructors() {
      const res = await fetch(`http://localhost:3001/fantasy/constructors`);
      const data = await res.json();
      console.log(data)
      this.allConstructors = data.constructors;
    }
  },
  async mounted() {
    await this.fetchDrivers();
    await this.fetchConstructors();
    this.ready = true;
  }
};
</script>

<style>

.driver-item {
  background: slategrey;
  height: 250px;
  width: 200px;
  border-radius: 20px;
}

.fantasy-grid {
  display: grid;
  grid-template-columns: minmax(70%, auto) minmax(auto, 600px);
  grid-template-rows: repeat(1, minmax(0, 1fr));
  height: 100%;
}

.team-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 40px 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
  height: 100%;
}

.grid-item{
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>