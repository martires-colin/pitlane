<template>
<div class="flex flex-col justify-center items-center">
    <div class="w-[60%] transition-opacity duration-400 ease-in ease-out pb-2" :class="{'opacity-30': fetching}">
        <v-table>
            <thead>
            <tr>
                <th class="text-left">
                Team Name
                </th>
                <th class="text-left">
                Owner
                </th>
                <th class="text-left">
                Points
                </th>
                <th></th>
            </tr>
            </thead>
            <tbody>
            <tr
                v-for="team in teams"
                :key="team.name"
            >
                <td class="text-left">{{ team.teamname }}</td>
                <td class="text-left">{{ team.owner }}</td>
                <td class="text-left">{{ team.points }}</td>
                <td>
                    <v-btn color="blue" class="mr-4" @click="$router.push(`${$route.path}/edit/${team.teamname}`)">Edit</v-btn>
                    <!-- <FormLeague :teamInfo="team"></FormLeague> -->
                    <v-btn color="danger" @click="deleteTeam(team.teamname)">Delete</v-btn>
                </td>
            </tr>
            </tbody>
        </v-table>
    </div>
    <v-pagination class="text-white" v-model="currentPage" :length="pageCount"></v-pagination>
</div>
</template>

<script>

export default {
    data() {
        return {
            teams: [],
            pageCount: 0,
            currentPage: 1,
            dialog: false,
        }
    },
    methods: {
        async fetchLeague() {
            const res = await fetch(`http://localhost:3001/fantasy/leagues/${this.$store.state.user.uid}/${this.$route.params.id}?page=1`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
                mode: 'cors'
            });
            const data = await res.json();
            this.teams = data.teams;
            this.pageCount = data.pages;
        },
        async deleteTeam(teamname) {
            const res = await fetch(`http://localhost:3001/fantasy/leagues/${this.$store.state.user.uid}/${this.$route.params.id}`, {
                method: 'DELETE',
                headers: {
                'Content-Type': 'application/json',
                },
                mode: 'cors',
                body: JSON.stringify({'leagueid': this.$route.params.id, 'teamname': teamname})
            });
            const data = await res.json();
            console.log(data)
            if (data.status == '200') {
                this.$router.go(-1)
            }
        }
    },
    async mounted() {
        await this.fetchLeague();
    }
}

</script>