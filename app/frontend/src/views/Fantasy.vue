<!-- Started by Anthony Ganci -->

<template>
  <div v-if="ready" class="fantasy flex flex-col h-full">
    <SelectFantasyTeam v-if="!teamSelected" :user-teams="userTeams" @set-selected-team="(setSelectedTeam)"></SelectFantasyTeam>
    <div v-if="teamSelected">
      <div class="flex flex-row justify-between p-3">
        <div class="rounded px-2">League: {{ leagueName }} </div>
        <div class="rounded px-2 flex flex-row">
          <p>Your Team: </p>
          <p class="pl-2 hover:underline underline-offset-4 cursor-pointer" @click="newNameDialog = true">{{ selectedTeam }}</p>
          <v-dialog v-model="newNameDialog" width="640px">
            <v-card>
              <v-card-title class="text-2xl">
                <span class="text-h5">Change Team Name</span>
              </v-card-title>
              <v-container>
                <v-row>
                  <v-col
                    cols="12"
                    sm="6"
                    md="12"
                  >
                    <v-text-field
                      label="Team name"
                      v-model="newTeamName"
                      required
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
              <v-card-actions >
                <v-spacer></v-spacer>
                <v-btn color="red" variant="tonal" @click="newNameDialog = false">Cancel</v-btn>
                <v-btn color="blue" variant="tonal" @click="updateTeamName">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </div>
        <div class="rounded px-2">Total points: {{ points }}</div>
      </div>
      <div class="flex flex-row justify-evenly px-10 py-2 pb-2 border-y border-gray-500">
        <div class="flex flex-row">
            <p class="text-red-500 pr-4">Previous Race</p>
            <img :src="$store.state.prevRace[3]" :alt="$store.state.prevRace[3]" class="h-[24px] w-[40px] border border-black"/>
            <p class="px-4">{{ $store.state.prevRace[0] }} </p>
            <p>{{ $store.state.prevRace[1] }} </p>
        </div>
        <div class="flex flex-row">
            <p class="text-green-500 pr-4">Next Race</p>
            <img :src="$store.state.nextRace[3]" :alt="$store.state.nextRace[3]" class="h-[24px] w-[40px] border border-black"/>
            <p class="px-4"> {{ $store.state.nextRace[0] }}</p>
            <p>{{ $store.state.nextRace[1] }} </p>
        </div>
      </div>
    </div>
      <div v-if="teamSelected" class="fantasy-grid h-full">
        <div class="flex flex-col justify-evenly">
          <div class="flex flex-row justify-evenly">
            <BCard
              :img-src="driver1Image"
              img-alt="Image"
              img-top
              tag="article"
              style="max-width: 20rem;"
              class="mb-2 bg-[#5b6068]">
              <p v-if="driver1 === ''" class="py-2">Add Driver</p>
              <FantasyModal button-title="+" :all-drivers="driverRoster" @set-driver1="(setDriver1)" v-if="driver1 === ''" />
              <BCardText class="text-xl">{{ driver1.drivername }}</BCardText>
              <FantasyModal button-title="Edit" :all-drivers="driverRoster" @set-driver1="(setDriver1)" v-if="driver1 !== ''" />
            </BCard>
            <BCard
              :img-src="driver2Image"
              img-alt="Image"
              img-top
              tag="article"
              style="max-width: 20rem;"
              class="mb-2 bg-[#5b6068]">
              <p v-if="driver2 === ''" class="py-2">Add Driver</p>
              <Driver2Modal button-title="+" :all-drivers="driverRoster" @set-driver2="(setDriver2)" v-if="driver2 === ''" />
              <BCardText class="text-xl">{{ driver2.drivername }}</BCardText>
              <Driver2Modal button-title="Edit" :all-drivers="driverRoster" @set-driver2="(setDriver2)" v-if="driver2 !== ''" />
            </BCard>
          </div>
          <div class="flex flex-row justify-center">
            <img :src="constructorImage" class="bg-[#5b6068] rounded-2 max-w-[500px] max-h-[300px]">
          </div>
          <div class="flex flex-row justify-center" v-if="lineupChanged">
            <button class="hover:bg-slate-400 p-2 rounded-2 text-xl bg-slate-500" @click="sendLineup">Save Lineup</button>
          </div>
        </div>
        <div v-if="whichSubTable === 0" class="leaderboard bg-[#282b30]">
          <div class="grid-item border-slate-300 hover:cursor-pointer" @click="whichSubTable = 0">Leaderboard</div>
          <div class="grid-item border-slate-300 hover:cursor-pointer" @click="whichSubTable = 1">Drivers</div>
          <div class="grid-item border-slate-300 hover:cursor-pointer" @click="whichSubTable = 2">Constructors</div>
          <div class="grid-item col-span-3" v-for="(team, index) in leaderboard" :key="index" >{{ index+1 }}. {{ team.name }} {{ team.points }} points</div>
        </div>
        <div v-if="whichSubTable === 1" class="bg-clip-content driver-grid bg-[#282b30]">
          <div class="grid-item border-slate-300 hover:cursor-pointer" @click="whichSubTable = 0">Leaderboard</div>
          <div class="grid-item border-slate-300 hover:cursor-pointer" @click="whichSubTable = 1">Drivers</div>
          <div class="grid-item border-slate-300 hover:cursor-pointer" @click="whichSubTable = 2">Constructors</div>
          <div class="grid-item col-span-3 border-slate-300" v-for="(driver, index) in allDrivers" :key="index">{{ driver }}</div>
        </div>
        <div v-if="whichSubTable === 2" class="bg-clip-content team-grid bg-[#282b30]">
          <div class="grid-item border-slate-300 hover:cursor-pointer" @click="whichSubTable = 0">Leaderboard</div>
          <div class="grid-item border-slate-300 hover:cursor-pointer" @click="whichSubTable = 1">Drivers</div>
          <div class="grid-item border-slate-300 hover:cursor-pointer" @click="whichSubTable = 2">Constructors</div>
          <div class="grid-item col-span-3 border-slate-300" v-for="(constructor, index) in allConstructors" :key="index">{{ constructor }}</div>
        </div>
      </div>
  </div>
  <Teleport to="body">
    <div class="d-flex justify-content-center w-100 fixed-top">
      <transition name="fade">
        <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showLineupError">
          Cannot have the same driver twice!
        </div>
      </transition>
    </div>
  </Teleport>
  <Teleport to="body">
    <div class="d-flex justify-content-center w-100 fixed-top">
      <transition name="fade">
        <div class="position-absolute top-10 alert alert-success text-center w-25" role="alert" v-if="showLineupSuccess">
          Lineup saved.
        </div>
      </transition>
    </div>
  </Teleport>
  <Teleport to="body">
    <div class="d-flex justify-content-center w-100 fixed-top">
      <transition name="fade">
        <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showNameError">
          Name must be a least 4 characters.
        </div>
      </transition>
    </div>
  </Teleport>
  <Teleport to="body">
    <div class="d-flex justify-content-center w-100 fixed-top">
      <transition name="fade">
        <div class="position-absolute top-10 alert alert-success text-center w-25" role="alert" v-if="showNameSuccess">
          Team name changed.
        </div>
      </transition>
    </div>
  </Teleport>
</template>

<script>
import FantasyModal from "../components/FantasyModal.vue";
import Driver2Modal from "@/components/Driver2Modal.vue";
import SelectFantasyTeam from "@/components/SelectFantasyTeam.vue";

export default {
  components: {
    FantasyModal,
    Driver2Modal,
    SelectFantasyTeam,
  },
  data() {
    return {
      allDrivers: ['Alexander Albon', 'Fernando Alonso', 'Valtteri Bottas', 'Nyck de Vries', 'Pierre Gasly', 'Lewis Hamilton', 'Nico Hülkenberg', 'Logan Sargeant', 'Charles Leclerc', 'Kevin Magnussen', 'Lando Norris', 'Esteban Ocon', 'Sergio Pérez', 'Oscar Piastri', 'George Russell', 'Carlos Sainz', 'Mick Schumacher', 'Lance Stroll', 'Yuki Tsunoda', 'Max Verstappen', 'Guanyu Zhou'],
      allConstructors: ['Alfa Romeo', 'AlphaTauri', 'Alpine F1 Team', 'Aston Martin', 'Ferrari', 'Haas F1 Team', 'McLaren', 'Mercedes', 'Red Bull', 'Williams'],
      ready: false,
      driver1: "",
      driver2: "",
      constructor: "",
      whichSubTable: 0,
      teamSelected: false,
      userTeams: [],
      selectedTeam: "",
      leagueName: "",
      leagueid: "",
      driverRoster: null,
      points: 0,
      lineupChanged: false,
      driver1Image: null,
      driver2Image: null,
      constructorImage: null,
      leaderboard: null,
      newTeamName: '',
      newNameDialog: false,
      showLineupError: false,
      showLineupSuccess: false,
      showNameError: false,
      showNameSuccess: false,
    }
  },
  methods: {
    async sendLineup() {
      console.log('hello')
      const res = await fetch('http://localhost:3001/fantasy/lineup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({'userid': this.$store.state.user.uid, 'leagueid': this.leagueid, 'driver1': this.driver1, 'driver2': this.driver2})
      });
      const data = await res.json();
      console.log(data)
      if (data.status == '200') {
        this.lineupChanged = false;
        this.triggerLineupSuccess();
      }
      if (data.status == '204') {
        this.triggerLineupError();
      }
    },
    triggerLineupError() {
      this.showLineupError = true;
      setTimeout(() => this.showLineupError = false, 2000)
    },
    triggerNameError() {
      this.showNameError = true;
      setTimeout(() => this.showNameError = false, 2000)
    },
    triggerNameSuccess() {
      this.showNameSuccess = true;
      setTimeout(() => this.showNameSuccess = false, 2000)
    },
    triggerLineupSuccess() {
      this.showLineupSuccess = true;
      setTimeout(() => this.showLineupSuccess = false, 2000)
    },
    setDriver1(obj) {
      console.log(obj)  
      console.log('string1')
      this.driver1 = obj;
      this.driver1Image = require(`@/assets/driverimages/${this.driver1.driverid}.png`)
      this.lineupChanged = true;
    },
    setDriver2(obj) {
      console.log('string2')
      this.driver2 = obj;
      this.driver2Image = require(`@/assets/driverimages/${this.driver2.driverid}.png`)
      this.lineupChanged = true;
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
        body: JSON.stringify({'userid': this.$store.state.user.uid}),
        mode: 'cors'
      });
      const data = await res.json();
      console.log(data)
      this.userTeams = data.teams;
      if (data.teams.length === 0) {
        this.$router.push('/fantasy/create')
      }
    },
    async setSelectedTeam(teamname, leagueid) {
      console.log(teamname, leagueid)
      this.selectedTeam = teamname;
      this.newTeamName = teamname;
      await this.fetchLeague(this.$store.state.user.uid, leagueid);
      await this.fetchTeamJSON(this.$store.state.user.uid, leagueid)
      this.teamSelected = true;
    },
    async fetchLeague(userid, leagueid) {
      const res = await fetch('http://localhost:3001/fantasy/league', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({'leagueid': leagueid, 'userid': userid})
      });
      const data = await res.json();
      console.log('league info', data)
      this.leaderboard = data.leaderboard;
      this.leagueName = data.leagueName;
      this.leagueid = leagueid;
    },
    async fetchTeamJSON(userid, leagueid) {
      const res = await fetch('http://localhost:3001/fantasy/team', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({'leagueid': leagueid, 'userid': userid})
      });
      const data = await res.json();
      console.log('userjson: ', data)
      this.driverRoster = data.driverRoster;
      this.driver1 = data.driver1;
      // need to add rookie drivers pics.
      this.driver1Image = require(`@/assets/driverimages/${this.driver1.driverid}.png`)
      this.driver2 = data.driver2;
      this.driver2Image = require(`@/assets/driverimages/${this.driver2.driverid}.png`)
      this.constructor = data.constructorName;
      this.constructorImage = require(`@/assets/constructorimages/${this.constructor.constructorid}.png`)
      this.points = data.points;
    },
    async updateTeamName() {
      if (this.newTeamName.length > 3) {
        this.newNameDialog = false;
        const res = await fetch('http://localhost:3001/fantasy/team', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          mode: 'cors',
          body: JSON.stringify({'leagueid': this.leagueid, 'userid': this.$store.state.user.uid,
           'teamname': this.selectedTeam, 'newTeamname': this.newTeamName})
        });
        const data = await res.json();
        this.selectedTeam = this.newTeamName;
        console.log(data)
        if (data.status === '200') {
          this.triggerNameSuccess();
        }
      }
      else {
        this.triggerNameError();
      }
    }
  },
  async mounted() {
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

.fantasy {
  
}

.leaderboard {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 40px auto;
  height: 100%;
}

.fantasy-grid {
  display: grid;
  grid-template-columns: minmax(70%, auto) minmax(auto, 600px);
  grid-template-rows: repeat(1, minmax(0, 1fr));
  /* height: full; */
  /* background-image: url('../assets/fantasy2.jpg');  
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  opacity: 100%; */
} 

.driver-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 40px auto;
  height: 100%;
}

.team-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 40px auto;
  height: 100%;
}

.grid-item {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.35s;
}

.grid-item:hover {
  background-color:#4b515a;
}
</style>