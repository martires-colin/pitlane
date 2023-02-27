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
        </b-input-group>
      </div>

      <div class="my-2">
        <button class="btn btn-secondary btn-md" id="update-btn" type="submit">Update Notification Preferences</button>
      </div>

    </form>

    
    <div class="container my-2">
      <div class="row mb-2">
        <div class="col-sm">
          <button class="btn btn-secondary btn-sm" id="simulate-btn" @click="simulateLightsOutNotif">Simulate "Lights Out!" Notification</button>
        </div>
        <div class="col-sm">
          <button class="btn btn-secondary btn-sm" id="simulate-btn" @click="simulateUpcomingRaceNotif">Simulate "Upcoming Race" Notification</button>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-sm">
          <button class="btn btn-secondary btn-sm" id="simulate-btn" @click="simulateCompleteResultsNotif">Simulate "Race Results" Notification</button>
        </div>
        <div class="col-sm">
          <button class="btn btn-secondary btn-sm" id="simulate-btn" @click="simulateDriverChampionshipStandingsNotif">Simulate "Driver Standings" Notification</button>
        </div>
      </div>
      <div class="row mb-2">
        <div class="col-sm">
          <button class="btn btn-secondary btn-sm" id="simulate-btn" @click="simulateConstructorChampionshipStandingsNotif">Simulate "Constructor Standings" Notification</button>
        </div>
      </div>
    </div>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-primary text-center w-25" role="alert" v-if="showAlert">
            Updated Notification Preferences!
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
    return { showAlert, triggerAlert }
  },
  data() {
    return {
      lightsOutNotif: this.$store.state.user.notificationPreferences.lightsOutNotif,
      upcomingRacesNotif: this.$store.state.user.notificationPreferences.upcomingRacesNotif,
      completeNotif: this.$store.state.user.notificationPreferences.completeNotif,
      driverStandingsNotif: this.$store.state.user.notificationPreferences.driverStandingsNotif,
      constructorStandingsNotif: this.$store.state.user.notificationPreferences.constructorStandingsNotif
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
      }
    },
    async simulateUpcomingRaceNotif() {      
      if (this.upcomingRacesNotif) {
        const data = await this.fetchUpcomingRace()
        console.log(data)
        console.log("Sending 'Upcoming Race!' Notification")
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
      }
    },
    async simulateCompleteResultsNotif() {
      if (this.completeNotif) {
        const data = await this.fetchCompleteResults()
        console.log(data)
        console.log("Sending 'Complete Race Results!' Notification")
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
      }
    },
    async simulateDriverChampionshipStandingsNotif() {
      if (this.driverStandingsNotif) {
        const data = await this.fetchDriverStandings()
        console.log(data)
        console.log("Sending 'Driver's Championship Standings!' Notification")
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
      }
    },
    async simulateConstructorChampionshipStandingsNotif() {
      if (this.constructorStandingsNotif) {
        const data = await this.fetchConstructorStandings()
        console.log(data)
        console.log("Sending 'Constructor's Championship Standings!' Notification")
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

#simulate-btn {
  color: white;
  background-color: rgb(160, 19, 19);
}

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

</style>