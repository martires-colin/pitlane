<script>
import router from '@/router';


// import { useStore} from "vuex";
export default {
    // setup() {
    //     const showDriversError = ref(false)
    //     const triggerDriversError= () => {
    //     showDriversError.value = true;
    //     setTimeout(() => showDriversError.value = false, 2000)

    //     return {
    //         showDriversError,
    //         triggerDriversError
    //     }
    // }
    // },
    data() {
        return {
            teamInformation: {
                teamname: "",
                userid: this.$store.state.user.uid,
                roster: {
                    d1: null,
                    d2: null,
                    d3: null,
                    d4: null,
                    d5: null,
                },
                constructorid: null,
                inviteCode: "",
                notificationFlag: true,
            },
            draftVisible: false,
            completeDraft: false,
            selected: [],
            options: ["Alexander Albon", "Fernando Alonso", "Valtteri Bottas", "Nyck de Vries", "Pierre Gasly", "Lewis Hamilton", "Nico Hülkenberg", "Logan Sargeant", "Charles Leclerc", "Kevin Magnussen", "Lando Norris", "Esteban Ocon", "Sergio Pérez", "Oscar Piastri", "George Russell", "Carlos Sainz", "Mick Schumacher", "Lance Stroll", "Yuki Tsunoda", "Max Verstappen", "Guanyu Zhou"],
            constructorOptions: ['Alfa Romeo', 'AlphaTauri', 'Alpine F1 Team', 'Aston Martin', 'Ferrari', 'Haas F1 Team', 'McLaren', 'Mercedes', 'Red Bull', 'Williams'],
            selectedConstructor: null,
            teamSuccess: false,
            paramCode: this.$route.params.inviteCode,
            showDriversError: false,
            showCreateError: false
        };
    },
    methods: {
        triggerDriversError() {
            this.showDriversError = true;
            setTimeout(() => this.showDriversError = false, 2000)
        },
        triggerCreateError() {
            this.showCreateError = true;
            setTimeout(() => this.showCreateError = false, 2000)
        },
        enterDraft() {
            if (this.teamInformation.inviteCode.length === 5 && this.teamInformation.teamname.length > 3) {
                this.draftVisible = true;
            }
        },
        async submitTeam(event) {
            event.preventDefault()
            if (this.selected.length === 5 && Boolean(this.selectedConstructor)) {
                this.teamInformation.roster.d1 = this.selected[0]
                this.teamInformation.roster.d2 = this.selected[1]
                this.teamInformation.roster.d3 = this.selected[2]
                this.teamInformation.roster.d4 = this.selected[3]
                this.teamInformation.roster.d5 = this.selected[4]
                this.teamInformation.constructorid = this.selectedConstructor
                await this.sendTeamInformation(this.teamInformation)
            }
            if (this.selected.length !== 5) {
                this.triggerDriversError()
            }
        },
        async sendTeamInformation(teamInformation) {
            console.log('HELLLOOOOOO')
            const res = await fetch('http://localhost:3001/fantasy/createTeam', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({'teamInformation': teamInformation}),
                mode: 'cors'
            });
            const data = await res.json();
            console.log(data)
            this.teamSuccess = data.success;
            if (this.teamSuccess === true) {
                router.push("/fantasy")
            }
            else {
                this.triggerCreateError();
            }
            // then redirect them to fantasy team page.
        }
    },
    computed: {
        inviteState() {
            return this.teamInformation.inviteCode.length === 5 ? true : false;
        },
        teamnameState(){
            return this.teamInformation.teamname.length > 3 ? true : false;
        },
        budget() {
            // console.log(this.selected.length > 2 ? true : false)
            // console.log(this.selected)
            // if (this.selected.length === 5){
            //     this.completeDraft = true;
            //     return true
            // }
            // else {
            //     return false
            // }
            return this.selected.length === 5 ? true : false;
        },
        invalidLineup() {
            if (this.selected.length < 5) {
                return `Select ${5- this.selected.length} more drivers.` 
            }
            if (this.selected.length > 5) {
                return 'Select ONLY 5 drivers!'
            }
            return 'Select 5 more drivers.'
        },
        constructorBudget() {
            return Boolean(this.selectedConstructor)
        },

    },
    mounted() {
        if (this.paramCode) {
            this.teamInformation.inviteCode = this.paramCode;
        }
    }
}
</script>

<template>
<div class="flex flex-col items-center h-full justify-center">
    <p v-if="!teamSuccess" class="text-xl pb-2">Join a League</p>
    <BForm @submit="enterDraft" class="flex flex-col items-center text-center" v-if="!draftVisible">
        <BFormInput class="w-[200px] mt-4 mb-2" :state="inviteState" required v-model="teamInformation.inviteCode" placeholder="Invite Code"></BFormInput>
        <BFormInvalidFeedback>Invite code must be 5 characters long.</BFormInvalidFeedback>
        <BFormInput trim class="w-[400px] mb-2 mt-2" v-model="teamInformation.teamname" :state="teamnameState" required placeholder="Team name"></BFormInput>
        <BFormInvalidFeedback class="mb-2">Team name must be at least 4 characters.</BFormInvalidFeedback>
        <BButton type="submit" class="bg-blue-500">Enter the draft</BButton>
    </BForm>
    <BForm @submit="submitTeam" class="flex flex-col items-center text-center" v-if="draftVisible && teamSuccess === false">
        <div class="flex flex-row space-x-8">
            <BFormGroup
                label="Drivers"
                v-slot="{ ariaDescribedby }"
                :invalid-feedback="invalidLineup"
                valid-feedback="Drivers Complete."
                :state="budget"
                >
                <BFormCheckboxGroup
                    v-model="selected"
                    :options="options"
                    :aria-describedby="ariaDescribedby"
                    :state="budget"
                    stacked=""
                >
                </BFormCheckboxGroup>
            </BFormGroup>
            <BFormGroup
                label="Constructors"
                v-slot="{ ariaDescribedby }"
                invalid-feedback="Select a constructor"
                valid-feedback="Constructor Complete."
                :state="constructorBudget"
                >
                <BFormRadioGroup
                    v-model="selectedConstructor"
                    :options="constructorOptions"
                    :aria-describedby="ariaDescribedby"
                    :state="constructorBudget"
                    stacked=""
                >
                </BFormRadioGroup>
            </BFormGroup>
        </div>
        <BButton type="submit" class="bg-blue-500">Create my team!</BButton>
    </BForm>
    <div v-if="teamSuccess">
        <p class="text-xl text-green-500">Team created!</p>
    </div>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showDriversError">
            You can only choose 5 drivers!
          </div>
        </transition>
      </div>
    </Teleport>

    <Teleport to="body">
      <div class="d-flex justify-content-center w-100 fixed-top">
        <transition name="fade">
          <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showCreateError">
            Error! Please try again.
          </div>
        </transition>
      </div>
    </Teleport>
</div>
</template>

<style>

</style>