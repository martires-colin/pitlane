<script>
export default {
    data() {
        return {
            leagues: null,
            pageCount: null,
            currentPage: 1,
            fetching: false,
        };
    },
    methods: {
        async fetchLeagues(page) {
            this.fetching = true;
            const res = await fetch(`http://localhost:3001/fantasy/leagues/${this.$store.state.user.uid}?page=${page}`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
                mode: 'cors'
            });
            const data = await res.json();
            console.log(data)
            this.leagues = data.leagues;
            this.pageCount = data.pages;
            this.fetching = false;
        },
        async fetchLeaguesAdmin(page) {
            this.fetching = true;
            const res = await fetch(`http://localhost:3001/admin/leagues/?page=${page}`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
                mode: 'cors'
            });
            const data = await res.json();
            console.log(data)
            this.leagues = data.leagues;
            this.pageCount = data.pages;
            this.fetching = false;
        }
    },
    async mounted() {
        //If user is admin run adminfetch
        // if(this.$store.getters.isAdmin){
        //     await this.fetchLeaguesAdmin(1);
        // }
        // else if (this.$store.getters.isLeagueOwner){
        //     await this.fetchLeagues(1);
        // }
        // console.log(this.$store.getters.isAdmin, this.$store.getters.isLeagueOwner)
        if (this.$store.getters.isLeagueOwner) {
            if (this.$store.getters.isAdmin) {
                await this.fetchLeaguesAdmin(1);
            }
            else await this.fetchLeagues(1);
        }
    },
    watch: {
        currentPage() {
            this.fetchLeaguesAdmin(this.currentPage);
        }
    }
};

</script>

<template>
<p class="text-xl text-[#00d4ff] py-4">
    Manage Leagues
</p>
<div class="flex flex-col justify-center items-center">
    <div class="w-[60%] transition-opacity duration-400 ease-in ease-out pb-2" :class="{'opacity-30': fetching}">
        <v-table hover>
            <thead>
            <tr>
                <th class="text-left">
                League Name
                </th>
                <th class="text-left">
                Member Count
                </th>
                <th class="text-left">
                Invite Code
                </th>
                <th class="text-left" v-if="$store.getters.isAdmin">
                League Owner
                </th>
            </tr>
            </thead>
            <tbody>
            <tr
                v-for="league in leagues"
                :key="league.name"
                @click="$router.push(`/fantasy/manage/${league.leagueID}`)"
            >
                <td class="text-left">{{ league.name }}</td>
                <td class="text-left">{{ league.members }}</td>
                <td class="text-left">{{ league.inviteCode }}</td>
                <td class="text-left" v-if="$store.getters.isAdmin">{{ league.owner }}</td>
            </tr>
            </tbody>
        </v-table>
    </div>
    <v-pagination class="text-white" v-model="currentPage" :length="pageCount"></v-pagination>
</div>
</template>