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
                <!-- img should retrieve photo from user object -->
                <!-- <img class="rounded-circle" src={{ $store.state.user.data }}" alt="Maxwell Admin"> -->
                <img class="rounded-circle" src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="Maxwell Admin">
              </div>
              

            <h5 class="user-name border border-danger">{{ $store.state.user.data.displayName }}</h5>
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

</style>