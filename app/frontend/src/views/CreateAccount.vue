<!-- By Colin Martires -->

<template>

  <div class="container  h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col col-xl-12">
        <div class="card" style="border-radius: 1rem; border: none;">
          <div class="row g-0">
            <div class="col-md-6 col-lg-5 d-none d-md-block">
              <img src="../assets/create-account-pic.jpg"
                alt="login form" class="img-fluid" style="border-radius: 1rem 0 0 1rem;" />
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
                    <!-- <label class="form-label">Name</label> -->
                    <input
                      type="text"
                      placeholder="Full Name"
                      class="form-control form-control-lg"
                      v-model="name"
                      required/>
                  </div>

                  <div class="form-outline mb-4">
                    <!-- <label class="form-label">Email address</label> -->
                    <input
                      type="email"
                      placeholder="Email"
                      class="form-control form-control-lg"
                      v-model="email"
                      required/>
                  </div>

                  <div class="form-outline mb-4">
                    <!-- <label class="form-label">Password</label> -->
                    <input
                    type="password"
                    placeholder="Password"
                    class="form-control form-control-lg"
                    v-model="password"
                    required/>
                  </div>

                  <div class="form-outline mb-4">
                    <!-- <label class="form-label">Password</label> -->
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

                  <!-- <a class="small text-muted" href="#!">Forgot password?</a> -->
                  <p class="mb-5 pb-lg-2" style="color: #393f81;">Already have an account? <a href="/login"
                      style="color: #393f81;">Login here</a></p>
                  <!-- <a href="#!" class="small text-muted">Terms of use.</a>
                  <a href="#!" class="small text-muted">Privacy policy</a> -->
                </form>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
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

      console.log(password.value)
      console.log(password2.value)

      if (password.value !== password2.value) {
        alert("Passwords do not match")
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
            alert("Email already in use");
            break;
          case "auth/invalid-email":
            alert("Invalid email");
            break;
          case "auth/operation-not-allowed":
            alert("Operation not allowed");
            break;
          case "auth/weak-password":
            alert("Weak password");
            break;
          default:
            alert("Something went wrong");
        }
        return;
      }
    }

    return { register, name, email, password, password2, error }

  }
};

</script>

<style>

#createAcc-btn {
  background-color: #005b96;
}

#createAcc-btn:hover {
  background-color: #03396c;
}

</style>