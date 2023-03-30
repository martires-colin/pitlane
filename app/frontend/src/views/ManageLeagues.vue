<script>
export default {
    data() {
        return {
            leagues: null,
        };
    },
    methods: {
        async fetchLeagues() {
            const res = await fetch(`http://localhost:3001/fantasy/leagues/${this.$store.state.user.uid}`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
                mode: 'cors'
            });
            const data = await res.json();
            console.log(data)
            this.leagues = data.leagues;
        },
        async fetchLeaguesAdmin(page) {
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
        }
    },
    async mounted() {
        //If user is admin run adminfetch
        await this.fetchLeaguesAdmin(1);
        // await this.fetchLeagues();
    }
};

</script>

<template>
<p>
    Manage Leagues
</p>
<div class="flex justify-center items-center">
    <div class="w-[80%]">
        <b-table class="text-white"
          id="my-table"
          :items="leagues"
          bordered="true"
          small
        ></b-table>
    </div>
    <!-- Pagination toolbar here -->
</div>
</template>