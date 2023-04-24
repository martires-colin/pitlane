<!-- By Colin Martires -->

<template>

  <v-container fluid fill-height>
    <v-row class="my-5" align="center" justify="center">
      <v-card width="80%">
        <v-toolbar color="blue-accent-2">
          <v-toolbar-title>Account Settings</v-toolbar-title>
        </v-toolbar>
        <div class="d-flex flex-row">
          <v-tabs
            v-model="tab"
            direction="vertical"
            color="blue-accent-2"
            width="20%"
            grow
          >
            <v-tab value="user-settings" width="20%">
              <v-icon
                size="large"
                color="blue-accent-2"
                icon="mdi-account"
              ></v-icon>
            </v-tab>
            <v-tab value="notification-settings" width="20%">
              <v-icon
                size="large"
                color="blue-accent-2"
                icon="mdi-message-text"
              ></v-icon>
            </v-tab>
          </v-tabs>
          <v-card width="40%">
            <v-card-item>
              <div class="py-4">
                <img :class="user.roles.isAdmin ? 'profile-pic-admin' : 'profile-pic'" :src="user.photoURL" alt="Profile Picture">
              </div>
              <v-divider></v-divider>
              <v-list>
                <v-list-item prepend-icon="mdi-account">
                  {{ user.displayName }}
                </v-list-item>
                <v-divider inset></v-divider>
                <v-list-item prepend-icon="mdi-phone">
                  {{ user.phoneNumber }}
                </v-list-item>
                <v-divider inset></v-divider>
                <v-list-item prepend-icon="mdi-email">
                  {{ user.email }}
                </v-list-item>
                <v-divider inset></v-divider>
              </v-list>
            </v-card-item>
          </v-card>
          <v-container fluid>
            <v-window v-model="tab">
              <v-window-item value="user-settings">
                <div class="container tab-content">
                  <UserSettings />
                </div>
              </v-window-item>
              <v-window-item value="notification-settings">
                <div class="container tab-content">
                  <NotificationSettings />
                </div>
              </v-window-item>       
            </v-window>
          </v-container>
        </div>
      </v-card>
    </v-row>
  </v-container>

</template>

<script>
import { useStore} from "vuex";
import {computed} from "vue";
import NotificationSettings from "@/components/NotificationSettings.vue"
import UserSettings from "@/components/UserSettings.vue"

export default {
  name: "Settings",
  components: {
    NotificationSettings,
    UserSettings
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
    return {
      tab: 'user-settings'
    }
  },
  methods: {
    async listUsers() {
      try {
        await this.$store.dispatch('listUsers')
      }
      catch (err) {
        console.log(err)
      }
    }
  }
}
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

.profile-pic-admin {
  display: inline-block;
  width: 150px;
  height: 150px;
  border-radius: 50em;
  border: 3px solid transparent;
  box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
  background: linear-gradient(rgb(255, 255, 255), rgb(255, 255, 255)) padding-box,
  radial-gradient( circle farthest-corner at 10% 20%,  rgba(97,186,255,1) 0%, rgba(166,239,253,1) 90.1% ) border-box;
  
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
  object-fit: cover;
}

.btab {
  background-color: #448AFF !important;
  color: white !important;
  
}

.btab-active {
  background-color:#212121 !important;
  color: white !important;

}

.tab-content {
  background-color: #212121;

}

.settings {
  border-radius: 50em;
  border: 3px solid transparent;
  box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
  background: linear-gradient(#212121, #212121) padding-box,
  radial-gradient( circle farthest-corner at 10% 20%,  rgba(97,186,255,1) 0%, rgba(166,239,253,1) 90.1% ) border-box;
}

.side-card {
  border-radius: 10px;
  border: 1px solid transparent;
  box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
  background: linear-gradient(#212121, #212121) padding-box,
  radial-gradient( circle farthest-corner at 10% 20%,  rgba(97,186,255,1) 0%, rgba(166,239,253,1) 90.1% ) border-box;
}

#update-btn {
  background-color: #90CAF9;
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