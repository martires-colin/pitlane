<script>
export default {
    data() {
        return {
            leagues: [],
            pageCount: null,
            currentPage: 1,
            fetching: false,
            newNameDialog: false,
        };
    },
    methods: {
        async fetchLeagues(page) {
            this.fetching = true;
            const res = await fetch(`https://pitlane-api.up.railway.app/fantasy/leagues/${this.$store.state.user.uid}?page=${page}`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
                mode: 'cors'
            });
            const data = await res.json();
            this.leagues = data.leagues;
            this.pageCount = data.pages;
            if (data.leagues.length === 0) {
                try {
                await this.$store.dispatch('updateRoles', {
                    isLeagueOwner: false
                })
                }
                catch (err) {
                    console.log(err)
                }  
                this.$router.push('/') 
            }
            this.fetching = false;
        },
        async fetchLeaguesAdmin(page) {
            this.fetching = true;
            const res = await fetch(`https://pitlane-api.up.railway.app/admin/leagues/?page=${page}`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
                mode: 'cors'
            });
            const data = await res.json();
            this.leagues = data.leagues;
            this.pageCount = data.pages;
            this.fetching = false;
        },
        async deleteLeague(leagueid) {
            const res = await fetch(`https://pitlane-api.up.railway.app/fantasy/leagues/${this.$store.state.user.uid}`, {
                method: 'DELETE',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({'leagueid': leagueid}),
                mode: 'cors'
            });
            const data = await res.json();
            if (data.status == '200') {
                if (this.$store.state.user.roles.isLeagueOwner) {
                    if (this.$store.state.user.roles.isAdmin) {
                    // if (this.isAdmin) {
                        await this.fetchLeaguesAdmin(1);
                    }
                    else await this.fetchLeagues(1);
                }
            }
        },
        async updateLeagueName() {
            this.newNameDialog = false;
            const res = await fetch('https://pitlane-api.up.railway.app/fantasy/league', {
                method: 'PUT',
                headers: {
                'Content-Type': 'application/json',
                },
                mode: 'cors',
                body: JSON.stringify({'leagueid': this.leagueid, 'newLeaguename': this.newLeaguename})
            });
            const data = await res.json();
            this.selectedTeam = this.newTeamName;
            console.log(data)
        }
    },
    async mounted() {
        if (this.$store.state.user.roles.isLeagueOwner) {
            if (this.$store.state.user.roles.isAdmin) {
            // if (this.isAdmin) {
                await this.fetchLeaguesAdmin(1);
            }
            else await this.fetchLeagues(1);
        }
        if (this.$store.state.user.roles.isAdmin) {
            await this.fetchLeaguesAdmin(1);
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
                <th class="text-left" v-if="$store.state.user.roles.isAdmin">
                League Owner
                </th>
                <th class="text-center">Actions</th>
            </tr>
            </thead>
            <tbody>
            <tr
                v-for="league in leagues"
                :key="league.name"
            >
                <td class="text-left" @click="newNameDialog = true">{{ league.name }}</td>
                <td class="text-left">{{ league.members }}</td>
                <td class="text-left">{{ league.inviteCode }}</td>
                <td class="text-left" v-if="$store.state.user.roles.isAdmin">{{ league.owner }}</td>
                <td class="text-center">
                    <v-btn color="blue" v-if="league.members !== 0" @click="$router.push(`/fantasy/manage/${league.leagueID}`)">Show</v-btn>
                    <v-btn color="danger" v-if="league.members === 0" @click="deleteLeague(league.leagueID)">Delete</v-btn>
                </td>
            </tr>
            </tbody>
        </v-table>
    </div>
    <p class="text-amber" v-if="(!fetching && leagues.length === 0)">You are not currently an owner of any leagues!</p>
    <v-pagination v-if="!(leagues.length === 0)" class="text-white" v-model="currentPage" :length="pageCount"></v-pagination>
</div>
</template>