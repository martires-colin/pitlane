<!-- By Colin Martires -->

<template>
  <div class="row py-2">
    <div class="mb-3">
      <h1>Receive notifications from PITLANE!</h1>
      <div v-if="this.$store.state.user.phoneNumber">
        <h1>Messages will be sent to {{ this.$store.state.user.phoneNumber }}</h1>
      </div>
    </div>
    <form @submit.prevent="updateNotificationPreferences">
      <div v-b-tooltip.hover title="Recieve a notification 15 minutes before a race starts!">
        <b-input-group class="mb-4">
          <b-input-group-prepend is-text>
            <b-form-checkbox switch class="mr-n2" v-model="lightsOutNotif">
              <span class="sr-only">Switch for Lights Out notification</span>
            </b-form-checkbox>
          </b-input-group-prepend>
          <b-form-input aria-label="Text input with switch" placeholder="Lights Out!" disabled></b-form-input>
          <b-input-group-append>
            <v-menu v-model="lightsOutPopUp" :close-on-content-click="false" location="end">
              <template v-slot:activator="{ props }">
                <v-btn color="blue-accent-2" v-bind="props" height="auto"  class="elevation-0">
                  <v-icon size="large" icon="mdi-information"></v-icon>
                </v-btn>
              </template>
              <v-card min-width="300">
                <div class="container p-3 text-center">
                  <div class="d-block">
                    <p>Recieve a notification 15 minutes before a race starts!</p>
                  </div>
                  <div class="container my-3 p-3 text-center rounded-lg message-example">
                    PITLANE<br>
                    Lights Out!<br>
                    The Bahrain Grand Prix starts in 15 minutes!
                  </div>
                  <div class="d-block pt-2">
                    <button class="btn btn-danger btn-sm" @click="simulateLightsOutNotif">Simulate "Lights Out!" Notification</button>
                  </div>
                </div>
              </v-card>
            </v-menu>
          </b-input-group-append>
        </b-input-group>
      </div>

      <div v-b-tooltip.hover title="Recieve a notification of the next race!">
        <b-input-group class="mb-4">
          <b-input-group-prepend is-text>
            <b-form-checkbox switch class="mr-n2" v-model="upcomingRacesNotif">
              <span class="sr-only">Switch for Upcoming Race notification</span>
            </b-form-checkbox>
          </b-input-group-prepend>
          <b-form-input aria-label="Text input with switch" placeholder="Upcoming Race" disabled></b-form-input>
          <b-input-group-append>
            <v-menu v-model="upcomingRacePopUp" :close-on-content-click="false" location="end">
              <template v-slot:activator="{ props }">
                <v-btn color="blue-accent-2" v-bind="props" height="auto"  class="elevation-0">
                  <v-icon size="large" icon="mdi-information"></v-icon>
                </v-btn>
              </template>
              <v-card min-width="300">
                <div class="container p-3 text-center">
                  <div class="d-block">
                    <p>Recieve a notification of the next race!</p>
                  </div>
                  <div class="container my-3 p-3 text-center rounded-lg message-example">
                    PITLANE<br>
                    Upcoming Race!<br>
                    Azerbaijan Grand Prix<br>
                    Date: 04-30-2023<br>
                    Time: 04:00 AM PST
                  </div>
                  <div class="d-block pt-2">
                    <button class="btn btn-danger btn-sm" @click="simulateUpcomingRaceNotif">Simulate "Upcoming Race" Notification</button>
                  </div>
                </div>
              </v-card>
            </v-menu>
          </b-input-group-append>
        </b-input-group>
      </div>

      <div v-b-tooltip.hover title="Recieve a notification of the most recent race results!">
        <b-input-group class="mb-4">
          <b-input-group-prepend is-text>
            <b-form-checkbox switch class="mr-n2" v-model="completeNotif">
              <span class="sr-only">Switch for Complete Race Results notification</span>
            </b-form-checkbox>
          </b-input-group-prepend>
          <b-form-input aria-label="Text input with switch" placeholder="Race Results" disabled></b-form-input>
          <b-input-group-append>
            <v-menu v-model="raceResultsPopUp" :close-on-content-click="false" location="end">
              <template v-slot:activator="{ props }">
                <v-btn color="blue-accent-2" v-bind="props" height="auto"  class="elevation-0">
                  <v-icon size="large" icon="mdi-information"></v-icon>
                </v-btn>
              </template>
              <v-card min-width="300">
                <div class="container p-3 text-center">
                  <div class="d-block">
                    <p>Recieve a notification of the most recent race results!</p>
                  </div>
                  <div class="container my-3 p-3 text-center rounded-lg message-example">
                    PITLANE<br>
                    Race Results for Australian Grand Prix<br>
                    1   Max Verstappen<br>
                    2   Lewis Hamilton<br>
                    3   Fernando Alonso<br>
                    4   Lance Stroll<br>
                    5   Sergio Pérez<br>
                    6   Lando Norris<br>
                    7   Nico Hülkenberg<br>
                    8   Oscar Piastri<br>
                    9   Guanyu Zhou<br>
                    10  Yuki Tsunoda<br>
                    11  Valtteri Bottas<br>
                    12  Carlos Sainz<br>
                    13  Pierre Gasly<br>
                    14  Esteban Ocon<br>
                    15  Nyck de Vries<br>
                    16  Logan Sargeant<br>
                    17  Kevin Magnussen<br>
                    18  George Russell<br>
                    19  Alexander Albon<br>
                    20  Charles Leclerc
                  </div>
                  <div class="d-block pt-2">
                    <button class="btn btn-danger btn-sm" @click="simulateCompleteResultsNotif">Simulate "Race Results" Notification</button>
                  </div>
                </div>
              </v-card>
            </v-menu>
          </b-input-group-append>
        </b-input-group>
      </div>

      <div v-b-tooltip.hover title="Recieve a notification of the current Driver's Championship standings!">
        <b-input-group class="mb-4">
          <b-input-group-prepend is-text>
            <b-form-checkbox switch class="mr-n2" v-model="driverStandingsNotif">
              <span class="sr-only">Switch for Driver's Championship Standings notification</span>
            </b-form-checkbox>
          </b-input-group-prepend>
          <b-form-input aria-label="Text input with switch" placeholder="Driver's Championship Standings" disabled></b-form-input>
          <b-input-group-append>
            <v-menu v-model="driversPopUp" :close-on-content-click="false" location="end">
              <template v-slot:activator="{ props }">
                <v-btn color="blue-accent-2" v-bind="props" height="auto"  class="elevation-0">
                  <v-icon size="large" icon="mdi-information"></v-icon>
                </v-btn>
              </template>
              <v-card min-width="300">
                <div class="container p-3 text-center">
                  <div class="d-block">
                    <p>Recieve a notification of the current Driver's Championship standings!</p>
                  </div>
                  <div class="container my-3 p-3 text-center rounded-lg message-example">
                    PITLANE<br>
                    Driver's Championship Standings<br>
                    1   Max Verstappen    69pts<br>
                    2   Sergio Pérez      54pts<br>
                    3   Fernando Alonso   45pts<br>
                    4   Lewis Hamilton    38pts<br>
                    5   Carlos Sainz      20pts<br>
                    6   Lance Stroll      20pts<br>
                    7   George Russell    18pts<br>
                    8   Lando Norris      8pts<br>
                    9   Nico Hülkenberg   6pts<br>
                    10  Charles Leclerc   6pts<br>
                    11  Valtteri Bottas   4pts<br>
                    12  Esteban Ocon      4pts<br>
                    13  Oscar Piastri     4pts<br>
                    14  Pierre Gasly      4pts<br>
                    15  Guanyu Zhou       2pts<br>
                    16  Yuki Tsunoda      1pts<br>
                    17  Kevin Magnussen   1pts<br>
                    18  Alexander Albon   1pts<br>
                    19  Logan Sargeant    0pts<br>
                    20  Nyck de Vries     0pts
                  </div>
                  <div class="d-block pt-2">
                    <button class="btn btn-danger btn-sm" @click="simulateDriverChampionshipStandingsNotif">Simulate "Driver Standings" Notification</button>
                  </div>
                </div>
              </v-card>
            </v-menu>
          </b-input-group-append>
        </b-input-group>
      </div>

      <div v-b-tooltip.hover title="Recieve a notification of the current Constructor's Championship standings!">
        <b-input-group class="mb-4">
          <b-input-group-prepend is-text>
            <b-form-checkbox switch class="mr-n2" v-model="constructorStandingsNotif">
              <span class="sr-only">Switch for Constructor's Championship Standings notification</span>
            </b-form-checkbox>
          </b-input-group-prepend>
          <b-form-input aria-label="Text input with switch" placeholder="Constructor's Championship Standings" disabled></b-form-input>
          <b-input-group-append>
            <v-menu v-model="constructorsPopUp" :close-on-content-click="false" location="end">
              <template v-slot:activator="{ props }">
                <v-btn color="blue-accent-2" v-bind="props" height="auto"  class="elevation-0">
                  <v-icon size="large" icon="mdi-information"></v-icon>
                </v-btn>
              </template>
              <v-card min-width="300">
                <div class="container p-3 text-center">
                  <div class="d-block">
                    <p>Recieve a notification of the current Constructor's Championship standings!</p>
                  </div>
                  <div class="container my-3 p-3 text-center rounded-lg message-example">
                    PITLANE<br>
                    Constructor's Championship Standings<br>
                    1   Red Bull     123pts<br>
                    2   Aston Martin 65pts<br>
                    3   Mercedes     56pts<br>
                    4   Ferrari      26pts<br>
                    5   McLaren      12pts<br>
                    6   Alpine F1 Team 8pts<br>
                    7   Haas F1 Team 7pts<br>
                    8   Alfa Romeo   6pts<br>
                    9   AlphaTauri   1pts<br>
                    10  WilliamsRacing 1pts
                  </div>
                  <div class="d-block pt-2">
                    <button class="btn btn-danger btn-sm" @click="simulateConstructorChampionshipStandingsNotif">Simulate "Constructor Standings" Notification</button>
                  </div>
                </div>
              </v-card>
            </v-menu>
          </b-input-group-append>
        </b-input-group>
      </div>

      <div class="my-2">
          <v-btn type="submit" color="blue-accent-2">Update Notification Preferences</v-btn>
      </div>
    </form>

    <!-- Alerts -->
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-primary text-center w-25" role="alert" v-if="showAlert">
            Updated Notification Preferences!
          </div>
        </transition>
      </div>
    </Teleport>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showError">
            User is not subscribed to this notification!
          </div>
        </transition>
      </div>
    </Teleport>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-primary text-center w-25" role="alert" v-if="showSending">
            Sending notification!
          </div>
        </transition>
      </div>
    </Teleport>

  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue"

export default {
  name: "NotificationSettings",
  setup() {
    const showAlert = ref(false)
    const triggerAlert = () => {
      showAlert.value = true;
      setTimeout(() => showAlert.value = false, 2000)
    }

    const showError = ref(false)
    const triggerError = () => {
      showError.value = true;
      setTimeout(() => showError.value = false, 2000)
    }

    const showSending = ref(false)
    const triggerSending = () => {
      showSending.value = true;
      setTimeout(() => showSending.value = false, 2000)
    }
    return { showAlert, triggerAlert, showError, triggerError, showSending, triggerSending }
  },
  data() {
    return {
      lightsOutNotif: this.$store.state.user.notificationPreferences.lightsOutNotif,
      upcomingRacesNotif: this.$store.state.user.notificationPreferences.upcomingRacesNotif,
      completeNotif: this.$store.state.user.notificationPreferences.completeNotif,
      driverStandingsNotif: this.$store.state.user.notificationPreferences.driverStandingsNotif,
      constructorStandingsNotif: this.$store.state.user.notificationPreferences.constructorStandingsNotif,
      lightsOutPopUp: false,
      lightsOutExample: false,
      upcomingRacePopUp: false,
      upcomingRaceExample: false,
      raceResultsPopUp: false,
      raceResultsExample: false,
      driversPopUp: false,
      driversExample: false,
      constructorsPopUp: false,
      constructorsExample: false
    }
  },
  methods: {
    updateNotificationPreferences() {
      try {
        this.$store.dispatch('updateNotifications', {
          lightsOutNotif: this.lightsOutNotif,
          upcomingRacesNotif: this.upcomingRacesNotif,
          completeNotif: this.completeNotif,
          driverStandingsNotif: this.driverStandingsNotif,
          constructorStandingsNotif: this.constructorStandingsNotif
        })
        console.log("Updated Notification Preferences")
        this.triggerAlert()
      }
      catch (err) {
        console.log(err)
        return;
      }
    },
    async simulateLightsOutNotif() {
      if (this.lightsOutNotif) {
        const data = await this.fetchLightsOut()
        console.log(data)
        console.log("Sending 'Lights Out!' Notification")
        this.triggerSending()
        const payload = {
          phoneNumber: this.$store.state.user.phoneNumber,
          msg_body : data.msg_body
        }
        const path = "http://localhost:3001/send_SMS"
        axios
          .post(path, payload)
          .then((res) => {
            console.log(res)
          })
          .catch((err) => {
            console.error(err)
          })
      } else {
        console.log("User not subscribed to 'Lights Out' Notifications")
        this.triggerError()
      }
    },
    async simulateUpcomingRaceNotif() {      
      if (this.upcomingRacesNotif) {
        const data = await this.fetchUpcomingRace()
        console.log(data)
        console.log("Sending 'Upcoming Race!' Notification")
        this.triggerSending()
        const payload = {
          phoneNumber: this.$store.state.user.phoneNumber,
          msg_body : data.msg_body
        }
        const path = "http://localhost:3001/send_SMS"
        axios
          .post(path, payload)
          .then((res) => {
            console.log(res)
          })
          .catch((err) => {
            console.error(err)
          })
      } else {
        console.log("User not subscribed to 'Upcoming Race' Notifications")
        this.triggerError()
      }
    },
    async simulateCompleteResultsNotif() {
      if (this.completeNotif) {
        const data = await this.fetchCompleteResults()
        console.log(data)
        console.log("Sending 'Complete Race Results!' Notification")
        this.triggerSending()
        const payload = {
          phoneNumber: this.$store.state.user.phoneNumber,
          msg_body : data.msg_body
        }
        const path = "http://localhost:3001/send_SMS"
        axios
          .post(path, payload)
          .then((res) => {
            console.log(res)
          })
          .catch((err) => {
            console.error(err)
          })
      } else {
        console.log("User not subscribed to 'Complete Race Results' Notifications")
        this.triggerError()
      }
    },
    async simulateDriverChampionshipStandingsNotif() {
      if (this.driverStandingsNotif) {
        const data = await this.fetchDriverStandings()
        console.log(data)
        console.log("Sending 'Driver's Championship Standings!' Notification")
        this.triggerSending()
        const payload = {
          phoneNumber: this.$store.state.user.phoneNumber,
          msg_body : data.msg_body
        }
        const path = "http://localhost:3001/send_SMS"
        axios
          .post(path, payload)
          .then((res) => {
            console.log(res)
          })
          .catch((err) => {
            console.error(err)
          })
      } else {
        console.log("User not subscribed to 'Driver's Championship Standings' Notifications")
        this.triggerError()
      }
    },
    async simulateConstructorChampionshipStandingsNotif() {
      if (this.constructorStandingsNotif) {
        const data = await this.fetchConstructorStandings()
        console.log(data)
        console.log("Sending 'Constructor's Championship Standings!' Notification")
        this.triggerSending()
        const payload = {
          phoneNumber: this.$store.state.user.phoneNumber,
          msg_body : data.msg_body
        }
        const path = "http://localhost:3001/send_SMS"
        axios
          .post(path, payload)
          .then((res) => {
            console.log(res)
          })
          .catch((err) => {
            console.error(err)
          })
      } else {
        console.log("User not subscribed to 'Constructor's Championship Standings' Notifications")
        this.triggerError()
      }
    },
    async fetchCompleteResults() {
      const res = await fetch(`http://localhost:3001/race_results_notif`);
      const data = await res.json();
      console.log(data)
      return data
    },
    async fetchDriverStandings() {
      const res = await fetch(`http://localhost:3001/driver_standings_notif`);
      const data = await res.json();
      console.log(data)
      return data
    },
    async fetchConstructorStandings() {
      const res = await fetch(`http://localhost:3001/constructor_standings_notif`);
      const data = await res.json();
      console.log(data)
      return data
    },
    async fetchUpcomingRace() {
      const res = await fetch(`http://localhost:3001/upcoming_race_notif`);
      const data = await res.json();
      console.log(data)
      return data
    },
    async fetchLightsOut() {
      const res = await fetch(`http://localhost:3001/lights_out_notif`);
      const data = await res.json();
      console.log(data)
      return data
    }
  }
}
</script>

<style>

.fade-enter-from {
  opacity: 0;
}
.fade-enter-to {
  opacity: 1;
}
.fade-enter-active {
  transition: all 0.5s ease;
}
.fade-leave-from {
  opacity: 1;
}
.fade-leave-to {
  opacity: 0;
}
.fade-leave-active {
  transition: all 0.5s ease;
}

.mr-n2 {
  cursor: pointer;
}

.message-example {
  border-radius: 50em;
  border: 2px solid transparent;
  box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
  background: linear-gradient(#212121, #212121) padding-box,
  radial-gradient( circle farthest-corner at 10% 20%,  rgba(97,186,255,1) 0%, rgba(166,239,253,1) 90.1% ) border-box;
}

</style>