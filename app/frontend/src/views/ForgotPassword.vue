<!-- By Colin Martires -->

<template>

  <div class="container h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col col-xl-12">
        <div class="card mx-5 mt-4" style="border-radius: 1rem 1rem 1rem 1rem; border: none;">
          <div class="row g-0">
            <div class="h-[85vh] col-md-6 col-lg-5 d-md-block overflow-hidden" style="border-radius: 1rem 0 0 1rem; border: none;">
              <img src="@/assets/forgot-password-pic.jpg"
                alt="login form" class="" style="border-radius: 1rem 0 0 1rem;" />
            </div>
            <div class="col-md-6 col-lg-7 d-flex align-items-center">
              <div class="card-body p-4 p-lg-5 text-black">

                <form class="login" @submit.prevent="sendPasswordReset">

                  <div class="d-flex align-items-center justify-content-center mb-3 pb-1">
                    <img
                      src="@/assets/PL.png"
                      alt="Website logo"
                      width="150"
                      height="150"
                    />
                  </div>

                  <h5 class="fw-normal mb-0 pb-3" style="letter-spacing: 1px;">Enter your email to reset your password</h5>

                  <div class="form-outline mb-4">
                    <label class="form-label">Email address</label>
                    <input
                      type="email"
                      placeholder="Email"
                      class="form-control form-control-lg"
                      v-model="email"
                      required/>
                  </div>

                  <div class="pt-1 mb-4">
                    <button class="btn btn-secondary btn-lg" id="login-btn" type="submit">Send Password Reset Email</button>
                  </div>

                  <p class=" py-lg-2" style="color: #393f81;">Ready to try again? <span class="hover:cursor-pointer" @click="$router.push('/login')"
                      style="color: #393f81;">Login here</span></p>
                  <p class=" py-lg-2" style="color: #393f81;">Don't have an account? <span class="hover:cursor-pointer" @click="$router.push('/create-account')"
                      style="color: #393f81;">Register here</span></p>

                </form>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-primary text-center w-25" role="alert" v-if="showAlert">
            Password reset email sent!
          </div>
        </transition>
      </div>
    </Teleport>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showError">
            Email not found!
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

export default {
  name: "ForgotPassword",
  setup() {
    const email = ref('')

    const sendPasswordReset = async () => {
      sendPasswordResetEmail(auth, email.value)
        .then(() => {
          console.log(`password reset email sent to ${email.value}`)
          triggerAlert()
        })
        .catch((error) => {
          const errorCode = error.code;
          const errorMessage = error.message;
          console.log(errorCode)
          console.log(errorMessage)
          triggerError()
        })

    }

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

    return { sendPasswordReset, email, showAlert, triggerAlert, showError, triggerError }

  }
}

</script>

<style>

#login-btn {
  background-color: #005b96;
}

#login-btn:hover {
  background-color: #03396c;
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
