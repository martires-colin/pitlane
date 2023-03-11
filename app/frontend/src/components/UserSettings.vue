<!-- By Colin Martires -->

<template>
  <div>

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
<!-- ------ update profile pic ----------- -->
    <form @submit.prevent="updateProfilePicture">
      <div class="row py-2">
        <div class="form-group">
          <label class="pb-1">Update Profile Picture</label>
          <input type="text" class="form-control" placeholder="Enter image url" v-model="img_url" required>
          <button class="btn btn-secondary btn-md" id="update-btn" type="submit">Update Profile Picture</button>
        </div>
      </div>
    </form>
<!-- ------------------------------------------ -->

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-primary text-center w-25" role="alert" v-if="showPhoneAlert">
            Updated Phone Number!
          </div>
        </transition>
      </div>
    </Teleport>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-primary text-center w-25" role="alert" v-if="showPicSuccess">
            Updated Profile Picture!
          </div>
        </transition>
      </div>
    </Teleport>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showPicFail">
            Photo URL too long!!
          </div>
        </transition>
      </div>
    </Teleport>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100">
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
</style>