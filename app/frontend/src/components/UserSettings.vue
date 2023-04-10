<!-- By Colin Martires -->

<template>
  <div>

    <!-- display account email and password reset button -->
    <div class="row py-2">
      <div class="col-8">
        <div class="form-group">
          <label class="pb-1 w-100 text-left">Email</label>
          <div class="input-group mb-2">
            <input type="text" class="form-control" :value="user.email" :disabled="true">
          </div>
        </div>
      </div>
      <div class="col-4">
        <label class="pb-1 w-100 text-center">Forgot your password?</label>
        <PasswordSettings />
      </div>
    </div>

    <!-- Update Username -->
    <form @submit.prevent="updateUsername">
      <div class="row py-2">
        <label class="pb-1 w-100 text-left">Username</label>
        <div class="col-8">
          <div class="form-group">
            <div class="input-group mb-2">
              <input type="text" class="form-control" id="input-form-border" placeholder="Enter image url" v-model="user.displayName" required>
            </div>
          </div>
        </div>
        <div class="col-4">
          <div class="input-group-append">
              <button class="btn btn-secondary btn-md w-100" id="update-btn" type="submit">Update Username</button>
          </div>
        </div>
      </div>
    </form>


    <!-- Update/Set Phone Number -->
    <form @submit.prevent="update">
      <div class="row py-2">
        <label class="pb-1 w-100 text-left" for="phone">Phone Number</label>
        <div class="col-8">
          <div class="form-group">
            <div class="input-group mb-2">
              <div v-if="user.phoneNumber" class="w-100">
                <cleave
                  type="tel"
                  v-model="phoneNumber"
                  :options="phoneOptions"
                  class="form-control w-100"
                  id="input-form-border"
                  :placeholder="user.phoneNumber">
                </cleave>
              </div>
              <div v-else class="w-100">
                <cleave
                  type="tel"
                  v-model="phoneNumber"
                  :options="phoneOptions"
                  class="form-control w-100"
                  id="input-form-border"
                  :placeholder="12312345678">
                </cleave>
              </div>
            </div>
          </div>
        </div>
        <div class="col-4">
          <div class="input-group-append">
            <div v-if="user.phoneNumber">
              <button class="btn btn-secondary btn-md w-100" id="update-btn" type="submit">Update Phone Number</button>
            </div>
            <div v-else>
              <button class="btn btn-secondary btn-md w-100" id="update-btn" type="submit">Add Phone Number</button>
            </div>
          </div>
        </div>
      </div>
    </form>

    <!-- ------ update profile pic ----------- -->
    <form @submit.prevent="updateProfilePicture">
      <div class="row py-2">
        <label class="pb-1 w-100 text-left">Update Profile Picture</label>
        <div class="col-8">
          <div class="form-group">
            <div class="input-group mb-2">
              <input type="text" class="form-control" id="input-form-border" placeholder="Enter image url" v-model="img_url" required>
            </div>
          </div>
        </div>
        <div class="col-4">
          <div class="input-group-append">
              <button class="btn btn-secondary btn-md w-100" id="update-btn" type="submit">Update Profile Picture</button>
          </div>
        </div>
      </div>
    </form>

    <!-- Pop-up alerts -->
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-primary text-center w-25" role="alert" v-if="showPhoneAlert">
            Updated Phone Number!
          </div>
        </transition>
      </div>
    </Teleport>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-primary text-center w-25" role="alert" v-if="showPicSuccess">
            Updated Profile Picture!
          </div>
        </transition>
      </div>
    </Teleport>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showPicFail">
            Photo URL too long!
          </div>
        </transition>
      </div>
    </Teleport>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-primary text-center w-25" role="alert" v-if="showUsernameSuccess">
            Updated Username!
          </div>
        </transition>
      </div>
    </Teleport>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showUsernameFail">
            Failed to update username!
          </div>
        </transition>
      </div>
    </Teleport>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showErrorSomething">
            Something went wrong!
          </div>
        </transition>
      </div>
    </Teleport>

  </div>
</template>

<script>
import { useStore} from "vuex";
import {computed} from "vue";
import { ref } from 'vue'
import Cleave from "vue-cleave-component"
import 'cleave.js/dist/addons/cleave-phone.us'
import PasswordSettings from "@/components/PasswordSettings.vue"


export default {
  name: "UserSettings",
  components: {
    Cleave,
    PasswordSettings
  },
  setup() {
    const store = useStore()

    const phoneNumber = ref('')
    
    const user = computed(() => {
      return store.getters.user
    })
    
    const update = async () => {
      console.log(phoneNumber.value)
      try {
        store.dispatch('updatePhoneNumber', {
          phoneNumber: phoneNumber.value
        })
        console.log("Updated Phone Number")
        triggerPhoneAlert()
      }
      catch (err) {
        console.log(err)
        return;
      }
    }

    const showPhoneAlert = ref(false)
    const triggerPhoneAlert = () => {
      showPhoneAlert.value = true;
      setTimeout(() => showPhoneAlert.value = false, 2000)
    }

    const showPicSuccess = ref(false)
    const triggerPicSuccess = () => {
      showPicSuccess.value = true;
      setTimeout(() => showPicSuccess.value = false, 2000)
    }

    const showPicFail = ref(false)
    const triggerPicFail = () => {
      showPicFail.value = true;
      setTimeout(() => showPicFail.value = false, 2000)
    }

    const showUsernameSuccess = ref(false)
    const triggerUsernameSuccess = () => {
      showUsernameSuccess.value = true;
      setTimeout(() => showUsernameSuccess.value = false, 2000)
    }

    const showUsernameFail = ref(false)
    const triggerUsernameFail = () => {
      showUsernameFail.value = true;
      setTimeout(() => showUsernameFail.value = false, 2000)
    }

    const showErrorSomething = ref(false)
    const triggerErrorSomething = () => {
      showErrorSomething.value = true;
      setTimeout(() => showErrorSomething.value = false, 2000)
    }

    return {
      user,
      update,
      phoneNumber,
      showPhoneAlert,
      triggerPhoneAlert,
      showPicSuccess,
      triggerPicSuccess,
      showPicFail,
      triggerPicFail,
      showUsernameSuccess,
      triggerUsernameSuccess,
      showUsernameFail,
      triggerUsernameFail,
      showErrorSomething,
      triggerErrorSomething
    }
  },
  data() {
    return {
      phoneOptions: {
        phone: true,
        phoneRegionCode: 'US',
        prefix: "+1"
      },
      img_url: ''
    }
  },
  methods: {
    async updateProfilePicture() {
      try {
        await this.$store.dispatch('updateProfilePicture', {
          photoURL: this.img_url
        })
        this.triggerPicSuccess()
      }
      catch (err) {
        console.log(err)
        switch (err.code) {
          case "auth/invalid-profile-attribute":
            this.triggerPicFail()
            break;
          default:
            this.triggerErrorSomething()
        }
        return;
      }
    },
    async updateUsername() {
      try {
        await this.$store.dispatch('updateUsername', 
          this.user.displayName
        )
        this.triggerUsernameSuccess()
      }
      catch (err) {
        console.log(err)
        switch (err.code) {
          case "auth/invalid-profile-attribute":
            this.triggerUsernameFail()
            break;
          default:
            this.triggerErrorSomething()
        }
        return;
      }
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

#input-group-btn {
  background-color: #00d4ff;
  color: black;
  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
  border: 0px;
}

#input-group-btn:hover {
  background-color: white;
  color: black;
}

#input-form-border {
  border: 0px !important;
}

</style>