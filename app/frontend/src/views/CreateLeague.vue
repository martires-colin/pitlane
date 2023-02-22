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
            const res = await fetch('http://localhost:3001/fantasy/createLeague', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                mode: 'cors',
                body: JSON.stringify({'userid': '12345678910', 'leagueName': this.leagueName})
            });
            const data = await res.json();
            console.log(data)
            this.inviteCode = data.inviteCode;
        }
    }
  }
</script>

<template>
    <div class="flex flex-col items-center h-screen justify-center">
    <p class="text-xl">Create a League</p>
    <BForm @submit="onSubmit">
        <BFormInput class="w-[400px] my-4" v-model="leagueName" placeholder="Choose a name for your league"></BFormInput>
        <BButton type="submit">Create my League</BButton>
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