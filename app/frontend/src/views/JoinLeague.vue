<script>
// import { useStore} from "vuex";
export default {
    data() {
        return {
            teamInformation: {
                teamname: "",
                userid: this.$store.state.user.uid,
                d1: null,
                d2: null,
                d3: null,
                d4: null,
                d5: null,
                constructorid: null,
                inviteCode: "",
            },
            draftVisible: false,
        }
    },
    methods: {
        enterDraft() {
            this.draftVisible = true;
        }
    }
}
</script>

<template>
<div class="flex flex-col items-center h-screen justify-center">
    <p class="text-xl">Join a League</p>
    <BForm @submit="enterDraft" class="flex flex-col items-center text-center" v-if="!draftVisible">
        <BFormInput class="w-[200px] mt-4 mb-2" v-model="teamInformation.inviteCode" placeholder="Invite Code"></BFormInput>
        <BFormInput class="w-[400px] mb-4 mt-2" v-model="teamInformation.teamname" placeholder="Team name"></BFormInput>
        <BButton type="submit">Enter the draft</BButton>
    </BForm>
    
    <p>
        <!-- {{ teamInformation.inviteCode }}
        {{ teamInformation.teamname }} -->
        <!-- {{ $store.state.user.uid }} -->
    </p>
</div>
</template>

<style>

</style>