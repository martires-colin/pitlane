<!-- By Anthony Ganci -->

<script>

export default {
    data() {
        return {

        }
    },
    methods: {

    },
    props: {
        userTeams: Array,
    }
}

</script>

<template>
<div class="flex flex-col justify-center h-screen items-center">
    <p class="mb-4">Your Teams:</p> 
    <div v-for="(team, index) in userTeams" :key="index" class="hover:cursor-pointer hover:text-red-500" @click="$emit('setSelectedTeam', team[0], team[1])"> {{ team[0] }}</div>
</div>
</template>

<style>

</style>