<!-- Data Visualization Page Implemented by Anthony Ganci -->

<template>
  <div flex flex-col justify-center h-full items-center>
    <div class="button-group">
      <button  class="fastf1-button" @click="(show = 1), (src = ''), (driverLabel = 'Driver 1')">
        Head-to-Head
      </button>
      <button  class="fastf1-button" @click="(show = 2), (src = '')">
        Gear Shifts
      </button>
      <button class="fastf1-button" @click="(show = 3), (src = ''), (driverLabel = 'Driver')">
        Speed Visualization
      </button>
    </div>
    <BForm v-if="show !== 0" @submit="onSubmitH2H" class="flex flex-col items-center text-center pb-4">
      <div class="flex flex-row items-center">
        <BFormGroup
        label="Year"
        class="pr-4"
        >
          <BFormSelect @change="changeYear($event)" v-model="form.year" >
            <BFormSelectOption v-for="n in 75" :value="2024-n" :key="2024-n"> {{ 2024-n }}</BFormSelectOption>
          </BFormSelect>
        </BFormGroup>
        <BFormGroup
        label="Circuit"
        >
          <BFormSelect v-model="form.track" :options="trackOptions">
          </BFormSelect>
        </BFormGroup>
      </div>
      <div class="flex flex-row items-center">
        <BFormGroup label="Driver 1" class="pr-4" v-if="show === 1 || show === 3">
          <BFormInput class="w-[200px]" required v-model="form.driver1" placeholder="Driver 1"></BFormInput>
        </BFormGroup>
        <BFormGroup 
        v-if="show === 1"
        label="Driver 2"
        >
          <BFormInput class="w-[200px]" required v-model="form.driver2" placeholder="Driver 2"></BFormInput>
        </BFormGroup>
      </div>
      <BFormGroup
        label="Session"
        v-slot="{ ariaDescribedby }"
        invalid-feedback="Select a session."
        >
        <BFormRadioGroup
            v-model="form.session"
            :options="['Race', 'Qualifiying']"
            :aria-describedby="ariaDescribedby"
        >
        </BFormRadioGroup>
      </BFormGroup>
      <!-- <BButton type="submit" class="bg-blue-500">        
        <div v-if="load" class="flex flex-row justify-center items-center tex-center" role="status">
            <svg aria-hidden="true" class="w-6 h-6 text-gray-200 animate-spin dark:text-gray-600 fill-white" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
            </svg>
            <span class="pl-2">Getting Graph</span>
        </div>
        <div v-else>
          Get Graph
        </div>
      </BButton> -->
      <v-btn
      @click="onSubmitH2H"
      :loading="load"
      color="blue"
      variant="elevated"
      >
        Get Graph
      </v-btn>
    </BForm>
    
    <div class="loading" v-if="load">
      <div></div>
      <div></div>
      <div></div>
    </div>
    <img  :src="src" v-if="src !== ''"/>
  </div>
</template>

<style>
/* body {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #353839;
} */
.button-group {
  padding: 20px;
}
.fastf1-button {
  /* // font-family: "Roboto Mono"; */
  font-size: 28px;
  text-align: center;
  margin: 5px;
  padding-inline: 8px;
  background-color: #4AA3D1;
  color: #0e1111;
  border-radius: 4px;
  cursor: pointer;
}
.fastf1-button:hover {
  background-color: #2a97cd;
}
.fastf1 {
  /* // font-family: "Roboto Mono"; */
  font-size: 20px;
  /* color: $darkish; */
}
.fastf1 input[type="text"],
select {
  font-size: 18px;
}
.fastf1 label {
  text-align: right;
}
.fastf1 input[type="submit"] {
  background-color: #ff2800;
  /* font-family: "Roboto Mono"; */
  font-size: 20px;
  border-radius: 4px;
  border-width: 1px;
  margin-top: 8px;
}
.loading {
    display: flex;
    justify-content: center;
}
.loading-item {
    width: 1rem;
    height: 1rem;
    margin: 2rem 0.3rem;
    background: #b3cde0;
    border-radius: 50%;
    animation: 0.9s bounce infinite alternate;
}
.loading-item:nth-child(2) {
    animation-delay: 0.3s;
}
.loading-item:nth-child(3) {
    animation-delay: 0.6s;
}
@keyframes bounce {
    to {
        opacity: 0.3;
        transform: translate3d(0, -1rem, 0);
    }
}
</style>

<script>
export default {
  name: "Pitlane",
  data() {
    return {
      src: "",
      show: 0,
      load: false,
      form: {
        driver1: "",
        driver2: "",
        track: "",
        year: 2022,
        session: "Race",
      },
      driverLabel: '',
      yearOptions: null,
      trackOptions: ['Monaco Grand Prix', 'British Grand Prix', 'Italian Grand Prix', 'Circuit de Spa-Francorchamps']
    };
  },
  methods: {
    async changeYear(event){
      console.log('event', event)
      const res = await fetch(`http://localhost:3001/races/${event}`, {
        method: 'GET'
      });
      const data = await res.json();
      this.trackOptions = data.raceNames
    },
    async sendForm(method) {
      this.load = true;
      const res = await fetch('http://localhost:3001/pitlane', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({'method': method, 'driver1': this.form.driver1, 'driver2': this.form.driver2, 'year': this.form.year, 'session': this.form.session, 'track': this.form.track})
      });
      const data = await res.json();
      this.show = 0;
      this.load = false;
      this.src = data.src;

    },
    initialForm() {
      (this.form.driver1 = ""),
        (this.form.driver2 = ""),
        (this.form.track = ""),
        (this.form.session = "Race"),
        (this.form.year = 2022);
    },
    async onSubmitH2H(e) {
      this.src = "";
      e.preventDefault();
      this.load = true;
      if (this.show === 1) {
        await this.sendForm("headtohead");
      }
      if (this.show === 2) {
        await this.sendForm("gearshift");
      }
      if (this.show === 3) {
        await this.sendForm("speedvisual");
      }
      this.initialForm();
    },
  },
  async created() {
    await this.changeYear(2022);
  },
};
</script>