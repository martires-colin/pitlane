<script>
export default {
    data() {
      return {
        leagueName: "",
        inviteCode: "",
      }
    },
    methods: {
        async onSubmit() {
            if (this.leagueName.length > 3) {
                const res = await fetch('https://pitlane-api.up.railway.app/fantasy/createLeague', {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    mode: 'cors',
                    body: JSON.stringify({'userid': this.$store.state.user.uid, 'leagueName': this.leagueName})
                });
                const data = await res.json();
                console.log(data)
                this.inviteCode = data.inviteCode;
            }
        }
    },
    computed: {
        nameState() {
            return this.leagueName.length > 3 ? true : false;
        }
    }
  }
</script>

<template>
    <div class="flex flex-col items-center h-screen justify-center">
        <p class="text-xl">Create a League</p>
        <BForm @submit="onSubmit">
            <BFormInput class="w-[400px]" :state="nameState" v-model="leagueName" placeholder="Choose a name for your league"></BFormInput>
            <BFormInvalidFeedback>Team name must be at least 4 characters long.</BFormInvalidFeedback>
            <BButton type="submit" class="mt-4 bg-blue-500">Create my League</BButton>
        </BForm>
        <div class="py-4" v-if="inviteCode !== ''">
            <p class="text-xl">Invite Code for your League:</p>
            <p class="text-xl text-green-500">{{ inviteCode }}</p>
            <p class="text-md opacity-75">Make sure to copy this!</p>
        </div>
    </div>
</template>

<style>

</style>