<!-- By Colin Martires -->

<template>

  <!-- what background color? -->
  <!-- <div class="bg-dark-300 h-100"> -->
  <div class="bg-black h-100">
    <!-- <div class="container"> -->
      <!-- <h1>{{ $store.state.user }}</h1> -->
      <!-- <h1>{{ user }}</h1> -->
<!--   
      <div class="row py-2 my-5">
        <h1>Account Settings</h1>
      </div>
  
      <div class="row py-2">
        <div class="col-xl-3 col-lg-3 col-md-12 col-sm-12 col-12">        
          <div class="card h-100">
            <div class="card-body">
                <div class="row py-2 text-center">
                  <div>
                    <img class="profile-pic" :src="user.photoURL" alt="Profile Picture">
                  </div>
                </div>
              <h5 class="user-name">{{ user.displayName }}</h5>
            </div>
          </div>
        </div>
        <div class="col-xl-9 col-lg-9 col-md-12 col-sm-12 col-12">
          <div class="card h-100">
            <div class="card-body">
                <div class="row py-2 text-center">

                </div>
            </div>
          </div>
        </div>
      </div>
    </div> -->
<!-- 
    <section class="py-5 my-5">

      <div class="container">
        <h1 class="mb-4">Account Settings</h1>
        <div class="rounded-lg d-block d-sm-flex" style="background: slategrey">
          <div class="side-nav border border-right">
            <div class="p-4">
              <img class="profile-pic" :src="user.photoURL" alt="Profile Picture">
              <h4 class="pt-4">{{ user.displayName }}</h4>
            </div>
            <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
              <a href="#account" class="nav-link active show" id="account-tab" data-toggle="pill" role="tab" aria-controls="account" aria-selected="true">Account</a>
              <a href="#password" class="nav-link" id="password-tab" data-toggle="pill" role="tab" aria-controls="password" aria-selected="false">Password</a>
              <a href="#notifications" class="nav-link" id="notifications-tab" data-toggle="pill" role="tab" aria-controls="notifications" aria-selected="false">Notifications</a>
            </div>
          </div>
          <div class="user-info" id="v-pills-tabContent">
            <div class="tab-pane fade active show" id="account" role="tabpanel" aria-labelledby="account-tab">
              <h1>Account Settings</h1>
              <h2>Account Settings</h2>
            </div>
            <div class="tab-pane fade" id="password" role="tabpanel" aria-labelledby="password-tab">
              <p>password</p>
            </div>
            <div class="tab-pane fade" id="notifications" role="tabpanel" aria-labelledby="notifications-tab">
              <p>notifications</p>
            </div>
          </div>
        </div>
      </div>
    </section> -->
<!-- 

    <section class="py-5 my-5">
      <div class="container">
        <h1 class="mb-4">Account Settings</h1>
        <div class="container rounded-lg bg-dark-300">
          <div class="row py-2">
            <div class="p-4">
              <img class="profile-pic" :src="user.photoURL" alt="Profile Picture">
              <h4 class="pt-3">{{ user.displayName }}</h4>
            </div>
          </div>
          <div class="row py-2" >
            <div class="p-0">
              <b-card no-body style="background-color: slategrey">
                <b-tabs pills card vertical nav-wrapper-class="w-25" class="align-text-center">
                  <b-tab class="w-100" title="Account" active title-item-class="">

                    <div class="row py-2">
                      <div class="form-group">
                        <label class="pb-1">Username</label>
                        <input type="text" class="form-control" :value="user.displayName">
                      </div>
                    </div>
                    <div class="row py-2">
                      <div class="form-group">
                        <label class="pb-1">Email</label>
                        <input type="text" class="form-control" :value="user.email">
                      </div>
                    </div>
                    <div class="row py-2">
                      <div class="form-group">
                        <label class="pb-1">PhoneNumber</label>
                        <input type="text" class="form-control" :value="user.number">
                      </div>
                    </div>

                  </b-tab>
                  <b-tab class="side-tabs" title="Password" title-item-class="w-100">
                    <b-card-text>Reset Password Functionality</b-card-text>
                  </b-tab>
                  <b-tab class="side-tabs" title="Notifications" title-item-class="w-100">
                    <b-card-text>Subscribe to notifications</b-card-text>
                  </b-tab>
                </b-tabs>
              </b-card>
            </div>
          </div>

        </div>
      </div>
    </section> -->


    <section class="py-5 my-5">
      <div class="container">
        
        <h1 class="p-5">Account Settings</h1>

        <div class="rounded-lg d-block bg-dark-300">

          <b-tabs content-class="mt-0" align="center" no-fade="true" :active-nav-item-class="'btab-active'" no-nav-style="true">
            <b-tab title="Account" :title-link-class="'btab'" active>
              <div class="container tab-content">
                <div class="row py-2">
                  <div class="col-4">
                    <div class="card-body">
                      <div class="row py-2 text-center">
                        <div>
                          <img class="profile-pic" :src="user.photoURL" alt="Profile Picture">
                        </div>
                      </div>
                    <h5 class="user-name">{{ user.displayName }}</h5>
                  </div>
                  </div>
                  <div class="col-8">
                    <div class="row py-2">
                      <div class="form-group">
                        <label class="pb-1">Username</label>
                        <input type="text" class="form-control" :value="user.displayName">
                      </div>
                    </div>
                    <div class="row py-2">
                      <div class="form-group">
                        <label class="pb-1">Email</label>
                        <input type="text" class="form-control" :value="user.email">
                      </div>
                    </div>
                    <div class="row py-2">
                      <div class="form-group">
                        <label class="pb-1">PhoneNumber</label>
                        <input type="text" class="form-control" :value="user.number">
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </b-tab>

            <b-tab title="Password" :title-link-class="'btab'">
              <div class="container tab-content">
                <div class="row py-2">
                  <div class="col-4">
                    <div class="card-body">
                      <div class="row py-2 text-center">
                        <div>
                          <img class="profile-pic" :src="user.photoURL" alt="Profile Picture">
                        </div>
                      </div>
                    <h5 class="user-name">{{ user.displayName }}</h5>
                  </div>
                  </div>
                  <div class="col-8">
                    <div class="row py-2">
                      <div class="form-group">
                        <label class="pb-1">Old Password</label>
                        <input type="text" class="form-control">
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
                    </div>
                  </div>
                </div>
              </div>
            </b-tab>

            <b-tab title="Notifications" :title-link-class="'btab'">
              <div class="container tab-content">
                <div class="row py-2">
                  <div class="col-4">
                    <div class="card-body">
                      <div class="row py-2 text-center">
                        <div>
                          <img class="profile-pic" :src="user.photoURL" alt="Profile Picture">
                        </div>
                      </div>
                    <h5 class="user-name">{{ user.displayName }}</h5>
                  </div>
                  </div>
                  <div class="col-8">
                    <div class="row py-2">
                      <p>Subscribe to notifications</p>
                    </div>
                  </div>
                </div>
              </div>
            </b-tab>

          </b-tabs>
        </div>
      </div>
    </section>

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
  color: white;
  padding: 1rem;
}

.profile-pic {
  display: inline-block;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 5px solid white;
  box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px; 
  
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
  object-fit: cover;
}

.btab {
  background-color: #4AA3D1 !important;
  color: white !important;
  
}

.btab-active {
  background-color:slategrey !important;
  color: white !important;


}

.tab-content {
  background-color: slategrey;
}

</style>