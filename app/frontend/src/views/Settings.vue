<!-- By Colin Martires -->

<template>
  <div class="bg-black h-100">

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

                    <form @submit.prevent="update">
                      <div class="row py-2">
                        <div class="form-group">
                          <label class="pb-1">Username</label>
                          <input type="text" class="form-control" :value="user.displayName" :disabled="true">
                        </div>
                      </div>
                      <div class="row py-2">
                        <div class="form-group">
                          <label class="pb-1">Email</label>
                          <input type="text" class="form-control" :value="user.email" :disabled="true">
                        </div>
                      </div>
                      <div v-if="user.phoneNumber">
                        <div class="row py-2">
                          <div class="form-group">
                            <div class="container">
                              <div class="row">
                                <label class="pb-1" for="phone">Phone Number</label>
                              </div>
                              <div class="row">
                                <input
                                class="form-control form-rounded"
                                type="tel"
                                id="phone"
                                name="phone"
                                pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
                                :placeholder="user.phoneNumber"
                                v-model="phoneNumber"
                                required>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div v-else>
                        <div class="row py-2">
                          <div class="form-group">
                            <div class="container">
                              <div class="row">
                                <label class="pb-1" for="phone">Phone Number</label>
                              </div>
                              <div class="row">
                                <input
                                class="form-control form-rounded"
                                type="tel"
                                id="phone"
                                name="phone"
                                pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
                                placeholder="702-877-1500"
                                v-model="phoneNumber"
                                required>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div v-if="user.phoneNumber">
                        <div class="my-2">
                          <button class="btn btn-secondary btn-md" id="update-btn" type="submit">Update Phone Number</button>
                        </div>
                      </div>
                      <div v-else>
                        <div class="my-2">
                          <button class="btn btn-secondary btn-md" id="update-btn" type="submit">Add Phone Number</button>
                        </div>
                      </div>
                    </form>
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
import { ref } from 'vue'


export default {
  name: "Settings",
  setup() {
    const store = useStore()

    const phoneNumber = ref('')
    
    const user = computed(() => {
      console.log(store.getters.user)
      return store.getters.user
    })
    
    const update = async () => {
      console.log(phoneNumber.value)
      try {
        store.dispatch('updatePhoneNumber', {
          phoneNumber: phoneNumber.value
        })
        console.log("Updated Phone Number")
      }
      catch (err) {
        console.log(err)
        return;
      }
    }
    return { user, update, phoneNumber }
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

#update-btn {
  background-color: #005b96;
}

#update-btn:hover {
  background-color: #03396c;
}

#phone {
  color: black
}

</style>