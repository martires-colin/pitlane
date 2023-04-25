<template>
  <div v-if="ready">
    <h2 id="title">Schedule for {{ season }} Formula One Season</h2>
    <RouterLink to="/schedule" class="bg-green-500 px-2 rounded-1" >Back</RouterLink>
    <div class="pt-6 flex flex-row justify-center">
      <table class="schedule">
        <tr id="header">
          <th id="race-name">Name</th>
          <th id="race-date">Date</th>
          <th id="race-time">Time</th>
        </tr>
        <tr v-for="(race, index) in schedule" :key="index">
          <td>{{race[0]}}</td>
          <td>{{race[1]}}</td>
          <td>{{race[2]}}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<style>
.years {
  margin-right: 1rem;
}
#header {
  border: 1px solid;
}
#race-name {
  border-right: 1px solid;
  min-width: 280px;
}
#race-date {
  border-right: 1px solid;
  min-width: 135px;
}
#race-time {
  min-width: 135px;
}
.schedule td {
  border-left: 1px solid;
  border-right: 1px solid;
  border-bottom: 1px solid;
  padding-right: 20px;
  padding-left: 20px;
  text-align: left;
}
</style>

<script>
export default {
  data() {
    return {
      schedule: [],
      season: this.$route.params.year,
      ready: false,
    }
  },
  methods: {
    async fetchSchedule(year) {
        const res = await fetch(`http://localhost:3001/schedule/${year}`);
        const data = await res.json();
        console.log(data)
        this.schedule = data.schedule;
    }
  },
  async mounted() {
    await this.fetchSchedule(this.season);
    this.ready = true;
  }
}
</script>

<!-- <script setup>
import { ref } from 'vue';
console.log(this.$route.params.year)
const year = this.$route.params.year;
const res = await fetch(`http://localhost:3001/schedule/${year}`);
const data = await res.json();

const schedule = ref(data.schedule);
const season = ref(data.season);
</script> -->