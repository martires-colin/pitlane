<!-- By Colin Martires -->
<!-- Table design by Anthony Ganci -->

<template>

  <div>
    <p class="text-xl text-[#00d4ff] py-4">
        Admin Console
    </p>
    <div class="flex flex-col justify-center items-center">
        <div class="w-[60%] transition-opacity duration-400 ease-in ease-out pb-2" :class="{'opacity-30': fetching}">
            <v-table hover>
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
                        <v-btn v-else color="blue" @click="addAdminRole(user.email)">Promote</v-btn>
                        <v-btn color="danger" @click="deleteUser(user.email, user.uid)">Delete</v-btn>        
                      </div>
                    </td>
                </tr>
                </tbody>
            </v-table>
        </div>
        <v-pagination class="text-white" v-model="currentPage" :length="pageCount"></v-pagination>
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
            User deleted!
          </div>
        </transition>
      </div>
    </Teleport>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-success text-center w-25" role="alert" v-if="showPromote">
            User granted admin privileges!
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
        users: null
    };
  },
  methods: {
    async deleteUser(userEmail, user_uid) {
      console.log(`Deleting ${userEmail}`)
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
      const listUsers = httpsCallable(functions, 'listUsers')
      listUsers().then(results => {
        console.log(results)
        this.users = results.data.listOfUsers.users
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