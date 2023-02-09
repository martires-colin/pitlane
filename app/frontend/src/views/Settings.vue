<!-- By Colin Martires -->

<template>
  <div class="container border border-danger">
    <!-- <h1>{{ $store.state.user }}</h1> -->
    <h1>{{ user }}</h1>

    <div class="row my-5">
      <h1>Account Settings</h1>
    </div>

    <div class="row border border-success">
      <div class="col-xl-3 col-lg-3 col-md-12 col-sm-12 col-12">        
        <div class="card h-100">
          <div class="card-body border border-danger">
              <div class="row text-center">
                <div>
                  <img class="profile-pic" :src="user.data.photoURL" alt="Profile Picture">
                </div>
              </div>
            <h5 class="user-name border border-danger">{{ user.data.displayName }}</h5>
          </div>
        </div>
      </div>
      <div class="col-xl-9 col-lg-9 col-md-12 col-sm-12 col-12">
        <div class="p-5 border">User Info</div>
      </div>
    </div>
  </div>
</template>

<script>
import { useStore} from "vuex";
import {computed} from "vue";

export default {
  name: "Settings",
  setup() {
    const store = useStore()
    
    const user = computed(() => {
      console.log(store.getters.user)
      return store.getters.user
    })
    
    return { user }
  },
  props: {
    test: String
  }

};
</script>

<style>

.user-name {
  color: black;
  padding: 1rem;
}

.user-email {
  color: black;
}

.profile-pic {
  display: inline-block;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 1px solid #555;

  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
  object-fit: cover;
}

</style>