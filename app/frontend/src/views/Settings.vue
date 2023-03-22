<!-- By Colin Martires -->

<template>

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

                <div class="col-8 px-5">
                  <UserSettings />
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
                <div class="col-8 text-center px-5">
                  <PasswordSettings />
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
                <div class="col-8 px-5">
                  <NotificationSettings />
                </div>
              </div>
            </div>
          </b-tab>
        </b-tabs>
      </div>
    </div>
  </section>

</template>

<script>
import { useStore} from "vuex";
import {computed} from "vue";
import NotificationSettings from "@/components/NotificationSettings.vue"
import PasswordSettings from "@/components/PasswordSettings.vue"
import UserSettings from "@/components/UserSettings.vue"

export default {
  name: "Settings",
  components: {
    NotificationSettings,
    PasswordSettings,
    UserSettings,
  },
  setup() {
    const store = useStore()

    const user = computed(() => {
      console.log(store.getters.user)
      return store.getters.user
    })
    return { user }
  },
  data() {

  },
  methods: {
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
  background: white; 
  
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
  object-fit: cover;
}

.btab {
  background-color: #00d4ff !important;
  color: black !important;
  
}

.btab-active {
  background-color:slategrey !important;
  color: white !important;

}

.tab-content {
  background-color: slategrey;
}

#update-btn {
  background-color: #00d4ff;
  color: black;
}

#update-btn:hover {
  background-color: white;
  color: black;
}

#phone {
  color: black
}

</style>