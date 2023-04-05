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
                        <button class="btn btn-secondary btn-sm" id="promote-btn" @click="addAdminRole(user.email)">Promote</button>
                        <button class="btn btn-secondary btn-sm" id="simulate-btn" @click="deleteUser(user.email, user.uid)">Delete</button>
                      </div>
                    </td>
                </tr>
                </tbody>
            </v-table>
        </div>
        <v-pagination class="text-white" v-model="currentPage" :length="pageCount"></v-pagination>
    </div>
  </div>
</template>

<script>
import { functions, db } from "../firebase";
// import { functions } from "../firebase";
import { httpsCallable } from 'firebase/functions';
import {
  doc,
  deleteDoc
} from "firebase/firestore";

export default {
  name: "AdminConsole",
  data() {
    return {
        users: null,
    };
  },
  methods: {
    async deleteUser(userEmail, user_uid) {
      console.log(`Deleting ${userEmail}`)
      const deleteUser = httpsCallable(functions, 'deleteUser')
      deleteUser(userEmail).then(results => {
        console.log(results.data.message)
        console.log(results.data.results)
      }).catch(err => {
        console.log(err)
      })
      // remove user from Firestore
      console.log(user_uid)
      const docRef = doc(db, "users", user_uid)
      // const docSnap = await deleteDoc(docRef)
      // if (docSnap.exists()) {
      //   console.log("Deleted User Document", docSnap.data());
      // } else {
      //   console.log("No such document")
      // }

      try {
        await deleteDoc(docRef);
        console.log("Deleted User Document", user_uid);
      } catch (e) {
        console.error("Error deleting document: ", e);
      }


    },
    async addAdminRole(userEmail) {
      console.log(`Promoting ${userEmail} to admin ...`)
      const addAdminRole = httpsCallable(functions, 'addAdminRole')
      addAdminRole(userEmail).then(results => {
        console.log(results.data.message)
        this.$store.dispatch('updateAdminRole')
      }).catch(err => {
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
      }
  }
}
</script>

<style>

#promote-btn {
  color: white;
  background-color: rgb(19, 160, 54);
}

</style>