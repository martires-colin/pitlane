<!-- By Colin Martires -->

<template>

  <div class="container h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col col-xl-12">
        <div class="card mx-5 mt-4" style="border-radius: 1rem 1rem 1rem 1rem; border: none;">
          <div class="row g-0">
            <div class="h-[85vh] col-md-6 col-lg-5 d-md-block overflow-hidden" style="border-radius: 1rem 0 0 1rem; border: none;">
              <img src="../assets/login-pic.jpg"
                alt="login form" class="" style="border-radius: 1rem 0 0 1rem;" />
            </div>
            <div class="col-md-6 col-lg-7 d-flex align-items-center">
              <div class="card-body p-4 p-lg-5 text-black">

                <form class="login" @submit.prevent="login">

                  <div class="d-flex align-items-center justify-content-center mb-3 pb-1">
                    <img
                      src="@/assets/PL.png"
                      alt="Website logo"
                      width="150"
                      height="150"
                    />
                  </div>

                  <h5 class="fw-normal mb-0 pb-3" style="letter-spacing: 1px;">Sign into your account</h5>

                  <div class="form-outline mb-4">
                    <label class="form-label">Email address</label>
                    <input
                      type="email"
                      placeholder="Email"
                      class="form-control form-control-lg"
                      v-model="email"
                      required/>
                  </div>

                  <div class="form-outline mb-4">
                    <label class="form-label">Password</label>
                    <input
                    type="password"
                    placeholder="Password"
                    class="form-control form-control-lg"
                    v-model="password"
                    required/>
                  </div>

                  <div class="pt-1 mb-4">
                    <button class="btn btn-secondary btn-lg" id="login-btn" type="submit">Login</button>
                  </div>

                  <a @click="$router.push('/forgot-password')" style="color: #393f81;">Forgot Password?</a>
                  <p class=" py-lg-2" style="color: #393f81;">Don't have an account? <a @click="$router.push('/create-account')"
                      style="color: #393f81;">Register here</a></p>

                </form>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Alerts -->
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showErrorPassword">
            Incorrect Password!
          </div>
        </transition>
      </div>
    </Teleport>
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showErrorEmail">
            User not found!
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
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: "Login",
  setup() {
    const email = ref('')
    const password = ref('')
    const error = ref(null)

    const store = useStore()
    const router = useRouter()

    const login = async () => {
      try {
        let response = await store.dispatch('login', {
          email: email.value,
          password: password.value
        })
        console.log(response)
        router.push('/')
      }
      catch (err) {
        console.log(err)
        switch (err.code) {
          case "auth/wrong-password":
            triggerErrorPassword()
            break;
          case "auth/user-not-found":
            triggerErrorEmail()
            break;
          default:
            triggerErrorSomething()
        }
        return;
      }
    }

    const showErrorPassword = ref(false)
    const triggerErrorPassword = () => {
      showErrorPassword.value = true;
      setTimeout(() => showErrorPassword.value = false, 2000)
    }

    const showErrorEmail = ref(false)
    const triggerErrorEmail = () => {
      showErrorEmail.value = true;
      setTimeout(() => showErrorEmail.value = false, 2000)
    }

    const showErrorSomething = ref(false)
    const triggerErrorSomething = () => {
      showErrorSomething.value = true;
      setTimeout(() => showErrorSomething.value = false, 2000)
    }

    return {
      login,
      email,
      password,
      error,
      showErrorPassword,
      triggerErrorPassword,
      showErrorEmail,
      triggerErrorEmail,
      showErrorSomething,
      triggerErrorSomething
    }

  }
}

</script>

<style>

#login-btn {
  /* background-color: #005b96; */
  background-color: #00d4ff !important;
  border: 0;
}

#login-btn:hover {
  /* background-color: #03396c; */
  background-color: #0a2540 !important;
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
