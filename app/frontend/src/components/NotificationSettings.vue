<!-- By Colin Martires -->

<template>
  <div class="row py-2">

    <div class="mb-3">
      <h1>Receive notifications from PITLANE!</h1>
    </div>

    <form @submit.prevent="updateNotificationPreferences">

      <b-input-group class="mb-4">
        <b-input-group-prepend is-text>
          <b-form-checkbox switch class="mr-n2" v-model="lightsOutNotif">
            <span class="sr-only">Switch for Lights Out notification</span>
          </b-form-checkbox>
        </b-input-group-prepend>
        <b-form-input aria-label="Text input with switch" placeholder="Lights Out!" disabled></b-form-input>
      </b-input-group>
  
      <b-input-group class="mb-4">
        <b-input-group-prepend is-text>
          <b-form-checkbox switch class="mr-n2" v-model="upcomingRacesNotif">
            <span class="sr-only">Switch for Upcoming Race notification</span>
          </b-form-checkbox>
        </b-input-group-prepend>
        <b-form-input aria-label="Text input with switch" placeholder="Upcoming Races" disabled></b-form-input>
      </b-input-group>
  
      <b-input-group class="mb-4">
        <b-input-group-prepend is-text>
          <b-form-checkbox switch class="mr-n2" v-model="completeNotif">
            <span class="sr-only">Switch for Complete Race Results notification</span>
          </b-form-checkbox>
        </b-input-group-prepend>
        <b-form-input aria-label="Text input with switch" placeholder="Complete Race Results" disabled></b-form-input>
      </b-input-group>
  
      <div class="my-2">
        <button class="btn btn-secondary btn-md" id="update-btn" type="submit">Update Notification Preferences</button>
      </div>

    </form>

    <div class="my-2">
      <button class="btn btn-secondary btn-md" id="update-btn" @click="simulateNotifications">Simulate Push Notifications</button>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "NotificationSettings",
  data() {
    return {
      lightsOutNotif: this.$store.state.user.notificationPreferences.lightsOutNotif,
      upcomingRacesNotif: this.$store.state.user.notificationPreferences.upcomingRacesNotif,
      completeNotif: this.$store.state.user.notificationPreferences.completeNotif
    }
  },
  methods: {
    async simulateNotifications() {
      
      console.log(this.lightsOutNotif)
      console.log(this.upcomingRacesNotif)
      console.log(this.completeNotif)

      let payload = {
        phoneNumber: this.$store.state.user.phoneNumber,
        preferences: {
           lightsOutNotif: this.lightsOutNotif,
           upcomingRacesNotif: this.upcomingRacesNotif,
           completeNotif: this.completeNotif
        }
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


    },
    updateNotificationPreferences() {
      try {
        this.$store.dispatch('updateNotifications', {
          lightsOutNotif: this.lightsOutNotif,
          upcomingRacesNotif: this.upcomingRacesNotif,
          completeNotif: this.completeNotif
        })
        console.log("Updated Notification Preferences")
      }
      catch (err) {
        console.log(err)
        return;
      }
    }
  }
}
</script>

<style>
</style>