<!-- By Colin Martires -->

<template>
  <div class="container">
    <!-- <div class="row py-2">
      <div class="form-group">
      <label class="pb-1">Old Password</label>
      <input type="password" class="form-control">
      </div>
    </div>
    <div class="row py-2">
        <div class="form-group">
        <label class="pb-1">New Password</label>
        <input type="text" class="form-control">
        </div>
    </div>
    <div class="row py-2">
        <div class="form-group">
        <label class="pb-1">Retype Password</label>
        <input type="text" class="form-control">
        </div>
    </div> -->

    <div class="pt-1 mb-4">
      <button class="btn btn-secondary btn-lg" id="login-btn" @click="sendPasswordResetEmail">Send Password Reset Email</button>
    </div>
  </div>
</template>

<script>

export default {
  name: "PasswordSettings",
  methods: {
    // make alert "sent email!"
    async sendPasswordResetEmail() {
      console.log('Sending password reset email.')
      try {
        this.$store.dispatch('sendPasswordResetEmail')
      } catch (err) {
        console.log(err)
        return;
      }     
    }
  }
}
</script>

<style>

</style>