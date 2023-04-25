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
            <BFormSelectOption v-for="n in 74" :value="2023-n" :key="2023-n"> {{ 2023-n }}</BFormSelectOption>
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
      <BButton type="submit" class="bg-blue-500">Get Graph</BButton>
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
// import axios from "axios";
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
      if (this.show === 1) {
        // const payload = {
        //   method: "headtohead",
        //   driver1: this.form.driver1,
        //   driver2: this.form.driver2,
        //   track: this.form.track,
        //   session: this.form.session,
        //   year: this.form.year,
        // };
        await this.sendForm("headtohead");
      }
      if (this.show === 2) {
        await this.sendForm("gearshift");
      }
      if (this.show === 3) {
        await this.sendForm("speedvisual");
      }
      this.load = true;
      this.initialForm();
    },
  },
  async created() {
    await this.changeYear(2022);
  },
};
</script>