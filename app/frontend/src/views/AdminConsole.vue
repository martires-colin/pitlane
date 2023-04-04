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
                        <button class="btn btn-secondary btn-sm" id="promote-btn">Promote</button>
                        <button class="btn btn-secondary btn-sm" id="simulate-btn">Delete</button>
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
export default {
  name: "AdminConsole",
  data() {
    return {
        users: null,
    };
  },
  async mounted() {
    try {
        await this.$store.dispatch('listUsers').then(results => {
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