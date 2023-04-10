<!-- By Colin Martires -->
<!-- Table design by Anthony Ganci -->

<template>

  <div>
    <p class="text-xl text-[#00d4ff] pb-4 pt-10">
        Admin Console
    </p>
    <div class="flex flex-col justify-center items-center">
        <div class="w-[60%] transition-opacity duration-400 ease-in ease-out pb-2" :class="{'opacity-30': fetching}">
            <v-table fixed-header height="75vh">
                <thead>
                <tr>
                    <th class="text-left">
                    Display Name
                    </th>
                    <th class="text-left">
                    Email
                    </th>
                    <th class="text-center">
                    Actions
                    </th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="user in users" :key="user.uid">
                    <td class="text-left">{{ user.displayName }}</td>
                    <td class="text-left">{{ user.email }}</td>
                    <td class="text-left">
                      <div class="d-flex justify-content-around">
                        <v-btn v-if="user.hasOwnProperty('customClaims')" color="green" width="100" id="disabled">Admin</v-btn>
                        <v-btn v-else color="blue" @click="targetUserEmail = user.email, targetUserUid = user.uid, admin_dialog = true">Promote</v-btn>
                        <v-btn color="danger" @click="targetUserEmail = user.email, targetUserUid = user.uid, delete_dialog = true">Delete</v-btn>
                      </div>
                    </td>
                </tr>
                </tbody>
            </v-table>
        </div>    

      <v-dialog v-model="delete_dialog" width="auto">
        <v-card>
          <v-card-text>
            Are you sure you want to delete {{this.targetUserEmail}}?
          </v-card-text>
          <div class="d-flex justify-content-center">
            <v-card-actions>
              <v-btn color="blue" variant="outlined" @click="delete_dialog = false">No</v-btn>
              <v-btn color="blue" variant="tonal" @click="deleteUser(this.targetUserEmail, this.targetUserUid), delete_dialog = false">Yes, I'm sure</v-btn>
            </v-card-actions>
          </div>
        </v-card>
      </v-dialog>

      <v-dialog v-model="admin_dialog" width="auto">
        <v-card>
          <v-card-text>
            Are you sure you want to make {{this.targetUserEmail}} an admin?
          </v-card-text>
          <div class="d-flex justify-content-center">
            <v-card-actions>
              <v-btn color="blue" variant="outlined" @click="admin_dialog = false">No</v-btn>
              <v-btn color="blue" variant="tonal" @click="addAdminRole(this.targetUserEmail), admin_dialog = false">Yes, I'm sure</v-btn>
            </v-card-actions>
          </div>
        </v-card>
      </v-dialog>

    </div>

    <!-- Pop-up validators -->
    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showErrorSomething">
            Something went wrong!
          </div>
        </transition>
      </div>
    </Teleport>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-success text-center w-25" role="alert" v-if="showDelete">
            {{ this.targetUserEmail }} deleted!
          </div>
        </transition>
      </div>
    </Teleport>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-success text-center w-25" role="alert" v-if="showPromote">
            {{ this.targetUserEmail }} granted admin privileges!
          </div>
        </transition>
      </div>
    </Teleport>


  </div>
</template>

<script>
import { ref } from 'vue'
import { functions, db } from "../firebase";
import { httpsCallable } from 'firebase/functions';
import {
  doc,
  deleteDoc
} from "firebase/firestore";

export default {
  name: "AdminConsole",
  setup() {
    const showErrorSomething = ref(false)
    const triggerErrorSomething = () => {
      showErrorSomething.value = true;
      setTimeout(() => showErrorSomething.value = false, 2000)
    }

    const showDelete = ref(false)
    const triggerDelete = () => {
      showDelete.value = true;
      setTimeout(() => showDelete.value = false, 2000)
    }

    const showPromote = ref(false)
    const triggerPromote = () => {
      showPromote.value = true;
      setTimeout(() => showPromote.value = false, 2000)
    }

    return {
      showErrorSomething,
      triggerErrorSomething,
      showDelete,
      triggerDelete,
      showPromote,
      triggerPromote
    }
  },
  data() {
    return {
        users: null,
        fetching: false,
        delete_dialog: false,
        admin_dialog: false,
        targetUserEmail: null,
        targetUserUid: null,
    };
  },
  methods: {
    async deleteUser(userEmail, user_uid) {
      this.delete_dialog = true
      this.targetUserEmail = userEmail
      this.targetUserUid = user_uid
      console.log(`Deleting ${userEmail} ${user_uid}`)

      const deleteUser = httpsCallable(functions, 'deleteUser')
      deleteUser(userEmail).then(results => {
        console.log(results.data.message)
        this.triggerDelete()
      }).catch(err => {
        console.log(err)
      })
      console.log(user_uid)
      const docRef = doc(db, "users", user_uid)
      try {
        await deleteDoc(docRef);
        console.log("Deleted User Document", user_uid);
      } catch (e) {
        this.triggerErrorSomething()
        console.error("Error deleting document: ", e);
      }
    },
    async addAdminRole(userEmail) {
      this.admin_dialog = true
      this.targetUserEmail = userEmail

      console.log(`Promoting ${userEmail} to admin ...`)
      const addAdminRole = httpsCallable(functions, 'addAdminRole')
      addAdminRole(userEmail).then(results => {
        this.triggerPromote()
        console.log(results.data.message)
        this.$store.dispatch('updateAdminRole')
      }).catch(err => {
        this.triggerErrorSomething()
        console.log(err)
      })
    },
  },
  async mounted() {
    try {
      this.fetching = true
      const listUsers = httpsCallable(functions, 'listUsers')
      listUsers().then(results => {
        console.log(results)
        this.users = results.data.listOfUsers.users
        this.fetching = false
      })
    }
    catch (err) {
      console.log(err)
      this.triggerErrorSomething()
    }
  }
}
</script>

<style>

#promote-btn {
  color: white;
  background-color: rgb(19, 160, 54);
}

#disabled {
  pointer-events: none;
}

</style>