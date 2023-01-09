<script>
import axios from 'axios';
export default {
  data() {
    return {
      msg: "Schedule",
      load: false,
      schedule: [],
      season: 2023,
    };
  },
  methods: {
    getSchedule() {
      const path = "http://127.0.0.1:5000/schedule";
      axios.get(path).then((response) => {
        console.log(response);
        if (response.status == 200) {
          this.schedule = response.data.schedule;
          this.season = response.data.season;
        }
      });
    },
    sendYear(payload) {
        const path = "http://127.0.0.1:5000/schedule";
        axios.post(path, payload).then((response) => {
            this.load = false;
            this.schedule = response.data.schedule;
        });
    },
    onSubmitYear(event) {
        this.schedule = [];
        this.season = parseInt(event.target.value);
        const payload = {
            season: this.season,
        };
        this.sendYear(payload);
        this.load = true;
    },
  },
  created() {
    this.getSchedule();
  },
};
</script>

<style lang="scss">
.loading {
  display: flex;
  justify-content: center;
  div {
    width: 1rem;
    height: 1rem;
    margin: 2rem 0.3rem;
    background: #b3cde0;
    border-radius: 50%;
    animation: 0.9s bounce infinite alternate;
    &:nth-child(2) {
      animation-delay: 0.3s;
    }
    &:nth-child(3) {
      animation-delay: 0.6s;
    }
  }
}
</style>

<template>
  <main>
    <h2>{{ msg }}</h2>
    <h3>{{ season }}</h3>
    <select @change="onSubmitYear($event)">
        <option v-for="n in 74" :value="n+1949" :key="n+1949">{{ n + 1949 }}</option>
    </select>
    <div class="loading" v-if="load">
      <div></div>
      <div></div>
      <div></div>
    </div>
    <div>
        <p v-for="(race, index) in schedule" :key="index">{{ race }}</p>
    </div>
  </main>
</template>