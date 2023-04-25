<!-- By Colin Martires -->

<template>

  <div class="container h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col col-xl-12">
        <div class="card mx-5 mt-4" style="border-radius: 1rem 1rem 1rem 1rem; border: none;">
          <div class="row g-0">
            <div class="h-[85vh] col-md-6 col-lg-5 d-md-block overflow-hidden" style="border-radius: 1rem 0 0 1rem; border: none;">
              <img src="../assets/create-account-pic.jpg"
                alt="login form" class="" style="border-radius: 1rem 0 0 1rem;" />
            </div>
            <div class="col-md-6 col-lg-7 d-flex align-items-center">
              <div class="card-body p-4 p-lg-5 text-black">
                <form class="login" @submit.prevent="register">
                  <div class="d-flex align-items-center justify-content-center mb-3 pb-1">
                    <img
                      src="@/assets/PL.png"
                      alt="Website logo"
                      width="150"
                      height="150"
                    />
                  </div>
                  <h5 class="fw-normal mb-0 pb-3" style="letter-spacing: 1px;">Create an account</h5>
                  <div class="form-outline mb-4">
                    <input
                      type="text"
                      placeholder="Username"
                      class="form-control form-control-lg"
                      v-model="name"
                      required/>
                  </div>
                  <div class="form-outline mb-4">
                    <input
                      type="email"
                      placeholder="Email"
                      class="form-control form-control-lg"
                      v-model="email"
                      required/>
                  </div>
                  <div class="form-outline mb-4">
                    <input
                    type="password"
                    placeholder="Password"
                    class="form-control form-control-lg"
                    v-model="password"
                    required/>
                  </div>
                  <div class="form-outline mb-4">
                    <input
                    type="password"
                    placeholder="Reenter Password"
                    class="form-control form-control-lg"
                    v-model="password2"
                    required/>
                  </div>
                  <div class="pt-1 mb-4">
                    <button class="btn btn-dark btn-lg btn-block" id="createAcc-btn" type="submit">Create Account</button>
                  </div>
                  <p class="mb-5 pb-lg-2 hover:cursor-pointer" style="color: #393f81;">Already have an account?
                    <a @click="$router.push('/login')" class="hover:cursor-pointer"
                      style="color: #393f81;">Login here
                    </a>
                  </p>
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
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showEmailError">
            Email already in use!
          </div>
        </transition>
      </div>
    </Teleport>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showEmailInvalid">
            Please enter a valid email!
          </div>
        </transition>
      </div>
    </Teleport>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showPasswordError">
            Use a stronger password!
          </div>
        </transition>
      </div>
    </Teleport>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showPasswordMismatch">
            Passwords do not match!
          </div>
        </transition>
      </div>
    </Teleport>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showSomethingError">
            Something went wrong, try again later!
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
  name: "CreateAccount",
  setup() {
    const name = ref('')
    const email = ref('')
    const password = ref('')
    const password2 = ref('')
    const error = ref(null)

    const store = useStore()
    const router = useRouter()

    const register = async () => {
      if (password.value !== password2.value) {
        triggerPasswordMismatch()
        return
      }

      try {
        await store.dispatch('register', {
          email: email.value,
          password: password.value,
          name: name.value
        })
        console.log("Registered User")

        router.push("/")
      }
      catch (err) {
        console.log(err)
        switch (err.code) {
          case "auth/email-already-in-use":
            triggerEmailError()
            break;
          case "auth/invalid-email":
            alert("Invalid email");
            triggerEmailInvalid()
            break;
          case "auth/operation-not-allowed":
            alert("Operation not allowed");
            break;
          case "auth/weak-password":
            triggerPasswordError()
            break;
          default:
            triggerSomethingError()
        }
        return;
      }
    }

    // Trigger Alerts
    const showEmailError = ref(false)
    const triggerEmailError = () => {
      showEmailError.value = true;
      setTimeout(() => showEmailError.value = false, 2000)
    }

    const showEmailInvalid = ref(false)
    const triggerEmailInvalid = () => {
      showEmailInvalid.value = true;
      setTimeout(() => showEmailInvalid.value = false, 2000)
    }

    const showPasswordError = ref(false)
    const triggerPasswordError = () => {
      showPasswordError.value = true;
      setTimeout(() => showPasswordError.value = false, 2000)
    }

    const showPasswordMismatch = ref(false)
    const triggerPasswordMismatch = () => {
      showPasswordMismatch.value = true;
      setTimeout(() => showPasswordMismatch.value = false, 2000)
    }

    const showSomethingError = ref(false)
    const triggerSomethingError = () => {
      showSomethingError.value = true;
      setTimeout(() => showSomethingError.value = false, 2000)
    }

    return {
      register,
      name,
      email,
      password,
      password2,
      error,
      showEmailError,
      triggerEmailError,
      showEmailInvalid,
      triggerEmailInvalid,
      showPasswordError,
      triggerPasswordError,
      showPasswordMismatch,
      triggerPasswordMismatch,
      showSomethingError,
      triggerSomethingError
    }
  }
};

</script>

<style>

#createAcc-btn {
  background-color: #00d4ff !important;
  border: 0;
}

#createAcc-btn:hover {
  background-color: #0a2540 !important;
}

</style>