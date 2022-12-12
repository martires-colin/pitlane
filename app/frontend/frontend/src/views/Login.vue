<template>
  <main>
    <h1>Login Page</h1>

    <section class="forms">
      <form class="login" @submit.prevent="login">
        <h2>Login</h2>
        <input
          type="email"
          placeholder="Email Address"
          v-model="login_form.email"
        />
        <input
          type="password"
          placeholder="Password"
          v-model="login_form.password"
        />
        <input type="submit" value="Login" />
      </form>
    </section>

    <a href="/create-account">Create an Account</a>
  </main>
</template>

<script>
import { ref } from "vue";
import { useStore } from "vuex";

export default {
  name: "Login",
  setup() {
    const login_form = ref({});
    const store = useStore();

    const login = () => {
      store.dispatch("login", login_form.value);
    };

    return {
      login_form,
      login,
    };
  },
};
</script>

<style></style>
