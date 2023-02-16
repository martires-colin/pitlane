<!-- Started by Anthony Ganci -->

<template>
  <div v-if="ready" class="flex flex-col h-screen">
    <SelectFantasyTeam v-if="!teamSelected" :user-teams="userTeams" @set-selected-team="(setSelectedTeam)"></SelectFantasyTeam>
    <div v-if="teamSelected">
      <div class="flex flex-row justify-between p-4">
        <h1> {{ leagueName }} </h1>
        <h1>Total points: 0</h1>
      </div>
      <div class="flex flex-row justify-evenly px-10 py-2 pb-2 border-t border-gray-500">
        <div class="flex flex-row">
            <p class="text-red-500 pr-4">Previous Race</p>
            <img :src="$store.state.prevRace[2]" :alt="$store.state.prevRace[3]" class="h-[24px] w-[40px]"/>
            <p class="px-4">{{ $store.state.prevRace[0] }} </p>
            <p>{{ $store.state.prevRace[1] }} </p>
        </div>
        <div class="flex flex-row">
            <p class="text-green-500 pr-4">Next Race</p>
            <img :src="$store.state.nextRace[2]" :alt="$store.state.nextRace[3]" class="h-[24px] w-[40px]"/>
            <p class="px-4"> {{ $store.state.nextRace[0] }}</p>
            <p>{{ $store.state.nextRace[1] }} </p>
        </div>
      </div>
    </div>
      <div v-if="teamSelected" class="fantasy-grid">
        <div class="bg-dark-300 flex flex-col justify-evenly">
          <div class="flex flex-row justify-evenly">
            <div class="driver-item">
              <p v-if="driver1 === ''" class="py-2">Add Driver</p>
              <FantasyModal button-title="+" :all-drivers="allDrivers" @set-driver1="(str) => driver1 = str" v-if="driver1 === ''" />
              <p class="pt-28 text-xl" v-if="driver1 !== ''">{{ driver1 }}</p>
              <FantasyModal button-title="Edit" :all-drivers="allDrivers" @set-driver1="(str) => driver1 = str" v-if="driver1 !== ''" />
            </div>
            <div class="driver-item">
              <p v-if="driver2 === ''" class="py-2">Add Driver</p>
              <Driver2Modal button-title="+" :all-drivers="allDrivers" @set-driver2="(str) => driver2 = str" v-if="driver2 === ''" />
                <!-- <FantasyModal :button-title="['+', 'two']" :all-drivers="allDrivers" @set-driver2="(str) => driver2 = str" v-if="driver2 === ''" /> -->
              <p class="pt-28 text-xl" v-if="driver2 !== ''">{{ driver2 }}</p>
              <Driver2Modal button-title="Edit" :all-drivers="allDrivers" @set-driver2="(str) => driver2 = str" v-if="driver2 !== ''" />
              <!-- <FantasyModal :for-driver="2" button-title="Edit" :all-drivers="allDrivers" @set-driver2="(str) => driver2 = str" v-if="driver2 !== ''" /> -->
            </div>
          </div>
          <div class="flex flex-row justify-center">
            <div class="bg-slate-500 h-32 w-50 rounded-[20px]">
              <p class="py-2">Add Constructor</p>
              <ConstructorModal button-title="+" :all-constructors="allConstructors" @set-constructor="(str) => constructor = str" v-if="constructor === ''"/>
              <p class="pt-2 text-xl" v-if="constructor !== ''">{{ constructor }}</p>
              <ConstructorModal button-title="Edit" :all-constructors="allConstructors" @set-constructor="(str) => constructor = str" v-if="constructor !== ''"/>
            </div>
          </div>
        </div>
        <div class="bg-dark-300">
          <div v-if="showDriversConstructors === true" class="bg-clip-content driver-grid bg-jelly-bean-500">
            <div class="grid-item bg-jelly-bean-900 border-x-2 border-t-2 border-jelly-bean-600 hover:cursor-pointer" @click="showDriversConstructors = true">Drivers</div>
            <div class="grid-item bg-jelly-bean-800 border-t-2 border-r-2 border-jelly-bean-600 hover:cursor-pointer" @click="showDriversConstructors = false">Constructors</div>
            <div class="grid-item col-span-2 border-x-2 border-t-2 border-jelly-bean-600" v-for="(driver, index) in allDrivers" :key="index">{{ driver }}</div>
          </div>
          <div v-if="showDriversConstructors === false" class="bg-clip-content team-grid bg-jelly-bean-500">
            <div class="grid-item bg-jelly-bean-800 border-x-2 border-t-2 border-jelly-bean-600 hover:cursor-pointer" @click="showDriversConstructors = true">Drivers</div>
            <div class="grid-item bg-jelly-bean-900 border-t-2 border-r-2 border-jelly-bean-600 hover:cursor-pointer" @click="showDriversConstructors = false">Constructors</div>
            <div class="grid-item col-span-2 border-x-2 border-t-2 border-jelly-bean-600" v-for="(constructor, index) in allConstructors" :key="index">{{ constructor }}</div>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
import FantasyModal from "../components/FantasyModal.vue";
import Driver2Modal from "@/components/Driver2Modal.vue";
import ConstructorModal from "@/components/ConstructorModal.vue";
import SelectFantasyTeam from "@/components/SelectFantasyTeam.vue";

export default {
  components: {
    FantasyModal,
    Driver2Modal,
    ConstructorModal,
    SelectFantasyTeam,
  },
  data() {
    return {
      allDrivers: ['Alexander Albon', 'Fernando Alonso', 'Valtteri Bottas', 'Nyck de Vries', 'Pierre Gasly', 'Lewis Hamilton', 'Nico Hülkenberg', 'Nicholas Latifi', 'Charles Leclerc', 'Kevin Magnussen', 'Lando Norris', 'Esteban Ocon', 'Sergio Pérez', 'Daniel Ricciardo', 'George Russell', 'Carlos Sainz', 'Mick Schumacher', 'Lance Stroll', 'Yuki Tsunoda', 'Max Verstappen', 'Sebastian Vettel', 'Guanyu Zhou'],
      allConstructors: ['Alfa Romeo', 'AlphaTauri', 'Alpine F1 Team', 'Aston Martin', 'Ferrari', 'Haas F1 Team', 'McLaren', 'Mercedes', 'Red Bull', 'Williams'],
      ready: false,
      driver1: "",
      driver2: "",
      constructor: "",
      showDriversConstructors: true,
      teamSelected: false,
      userTeams: [],
      selectedTeam: "",
      leagueName: "",
    }
  },
  methods: {
    setDriver1(str) {
      console.log(str)  
      console.log('string1')
      this.driver1 = str;
      // console.log(this.allDrivers)
      // this.allDrivers.splice(this.allDrivers.indexOf(str), 1);
      // console.log(this.allDrivers)
    },
    setDriver2(str) {
      console.log('string2')
      this.driver2 = str;
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
    },
    async fetchUserTeams() {
      console.log('grabbing teams')
      const res = await fetch('http://localhost:3001/fantasy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({'userid': '12345678910'}),
        mode: 'cors'
      });
      const data = await res.json();
      console.log(data)
      this.userTeams = data.teams;
    },
    async setSelectedTeam(teamname, leagueid) {
      console.log(teamname, leagueid)
      this.selectedTeam = teamname;
      await this.fetchLeague(leagueid);
      this.teamSelected = true;
    },
    async fetchLeague(leagueid) {
      const res = await fetch('http://localhost:3001/fantasy/league', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({'leagueid': leagueid})
      });
      const data = await res.json();
      console.log('league info', data)
      this.leagueName = data.leagueName;
    },
  },
  async mounted() {
    // will eventually be fetching drivers/constructors available to user
    // await this.fetchDrivers();
    // await this.fetchConstructors();
    await this.fetchUserTeams();
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

.driver-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 40px auto;
  height: 100%;
}

.team-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 40px auto;
  height: 100%;
}

.grid-item{
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>