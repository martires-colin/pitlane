<!-- By Colin Martires -->

<template>
  <div>
    <button class="btn btn-secondary btn-md w-100" id="update-btn" @click="sendPasswordResetEmail">Send Password Reset Email</button>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-primary text-center w-25" role="alert" v-if="showAlert">
            Password reset email sent to {{ userEmail }}!
          </div>
        </transition>
      </div>
    </Teleport>
  </div>

</template>

<script>
import { ref } from 'vue'
import { auth } from "../firebase";
import { sendPasswordResetEmail } from 'firebase/auth'
import { useStore} from "vuex";
import {computed} from "vue";


export default {
  name: "PasswordSettings",
  components: {
  },
  setup() {
    const showAlert = ref(false)
    const triggerAlert = () => {
      showAlert.value = true;
      setTimeout(() => showAlert.value = false, 2000)
    }

    const store = useStore()
    const userEmail = computed(() => {
      return store.getters.user.email
    })

    return { showAlert, triggerAlert, userEmail }
  },
  methods: {
    async sendPasswordResetEmail() {
      console.log('Sending password reset email.')

      const user = auth.currentUser;
      sendPasswordResetEmail(auth, user.email)
        .then(() => {
          console.log("password reset email sent!")
        })
        .catch((error) => {
          const errorCode = error.code;
          const errorMessage = error.message;
          console.log(errorCode)
          console.log(errorMessage)
        })
      this.triggerAlert()  
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