<template>
    <p class="text-xl text-[#00d4ff] py-4">
        League: {{ leagueName }}
    </p>
    <router-view></router-view>
</template>

<script>
export default {
    data() {
        return {
            leagueName: null,
        }
    },
    methods: {
        async fetchLeagueName() {
            const res = await fetch(`http://localhost:3001/fantasy/leagues/${this.$store.state.user.uid}/${this.$route.params.id}?name=true`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
                mode: 'cors'
            });
            const data = await res.json();
            console.log(data)
            this.leagueName = data.leagueName;
        }
    },
    async mounted() {
        await this.fetchLeagueName();
    }
}
</script>