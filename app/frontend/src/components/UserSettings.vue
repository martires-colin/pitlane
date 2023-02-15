<!-- By Colin Martires -->

<template>

  <form @submit.prevent="update">
    <div class="row py-2">
      <div class="form-group">
        <label class="pb-1">Username</label>
        <input type="text" class="form-control" :value="user.displayName" :disabled="true">
      </div>
    </div>
    <div class="row py-2">
      <div class="form-group">
        <label class="pb-1">Email</label>
        <input type="text" class="form-control" :value="user.email" :disabled="true">
      </div>
    </div>
    <div v-if="user.phoneNumber">
      <div class="row py-2">
        <div class="form-group">
          <div class="container">
            <div class="row">
              <label class="pb-1" for="phone">Phone Number: {{ user.phoneNumber }}</label>
            </div>
            <div class="row">

              <!-- <input
              class="form-control form-rounded"
              type="tel"
              id="phone"
              name="phone"
              pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
              :placeholder="user.phoneNumber"
              v-model="phoneNumber"
              required> -->

              <cleave
              type="tel"
              v-model="phoneNumber"
              :options="phoneOptions"
              class="form-control"
              :placeholder="user.phoneNumber"
              >
              </cleave>

            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="row py-2">
        <div class="form-group">
          <div class="container">
            <div class="row">
              <label class="pb-1" for="phone">Phone Number</label>
            </div>
            <div class="row">

              <!-- <input
              class="form-control form-rounded"
              type="tel"
              id="phone"
              name="phone"
              pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
              placeholder="123-456-7890"
              v-model="phoneNumber"
              required> -->

              <cleave
              type="tel"
              v-model="phoneNumber"
              :options="phoneOptions"
              class="form-control"
              :placeholder="12312345678">
              </cleave>

            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="user.phoneNumber">
      <div class="my-2">
        <button class="btn btn-secondary btn-md" id="update-btn" type="submit">Update Phone Number</button>
      </div>
    </div>
    <div v-else>
      <div class="my-2">
        <button class="btn btn-secondary btn-md" id="update-btn" type="submit">Add Phone Number</button>
      </div>
    </div>
  </form>

</template>

<script>
import { useStore} from "vuex";
import {computed} from "vue";
import { ref } from 'vue'
import Cleave from "vue-cleave-component"
import 'cleave.js/dist/addons/cleave-phone.us'

export default {
  name: "UserSettings",
  components: {
    Cleave
  },
  setup() {
    const store = useStore()

    const phoneNumber = ref('')
    
    const user = computed(() => {
      console.log(store.getters.user)
      return store.getters.user
    })
    
    const update = async () => {
      console.log(phoneNumber.value)
      try {
        store.dispatch('updatePhoneNumber', {
          phoneNumber: phoneNumber.value
        })
        console.log("Updated Phone Number")
      }
      catch (err) {
        console.log(err)
        return;
      }
    }
    return { user, update, phoneNumber }
  },
  data() {
    return {
      phoneOptions: {
        phone: true,
        phoneRegionCode: 'US',
        prefix: "+1"
      }
    }
  },
  methods: {
  }
}
</script>

<style>

</style>