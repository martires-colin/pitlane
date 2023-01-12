<script>
import axios from 'axios';
export default {
  data() {
    return {
      load: false,
      schedule: [ [ "Bahrain Grand Prix", "2023-03-05", "15:00:00Z" ], [ "Saudi Arabian Grand Prix", "2023-03-19", "17:00:00Z" ], [ "Australian Grand Prix", "2023-04-02", "05:00:00Z" ], [ "Azerbaijan Grand Prix", "2023-04-30", "11:00:00Z" ], [ "Miami Grand Prix", "2023-05-07", "19:30:00Z" ], [ "Emilia Romagna Grand Prix", "2023-05-21", "13:00:00Z" ], [ "Monaco Grand Prix", "2023-05-28", "13:00:00Z" ], [ "Spanish Grand Prix", "2023-06-04", "13:00:00Z" ], [ "Canadian Grand Prix", "2023-06-18", "18:00:00Z" ], [ "Austrian Grand Prix", "2023-07-02", "13:00:00Z" ], [ "British Grand Prix", "2023-07-09", "14:00:00Z" ], [ "Hungarian Grand Prix", "2023-07-23", "13:00:00Z" ], [ "Belgian Grand Prix", "2023-07-30", "13:00:00Z" ], [ "Dutch Grand Prix", "2023-08-27", "13:00:00Z" ], [ "Italian Grand Prix", "2023-09-03", "13:00:00Z" ], [ "Singapore Grand Prix", "2023-09-17", "12:00:00Z" ], [ "Japanese Grand Prix", "2023-09-24", "05:00:00Z" ], [ "Qatar Grand Prix", "2023-10-08", "14:00:00Z" ], [ "United States Grand Prix", "2023-10-22", "19:00:00Z" ], [ "Mexico City Grand Prix", "2023-10-29", "20:00:00Z" ], [ "São Paulo Grand Prix", "2023-11-05", "18:00:00Z" ], [ "Las Vegas Grand Prix", "2023-11-18", "13:00:00Z" ], [ "Abu Dhabi Grand Prix", "2023-11-26", "13:00:00Z" ] ],
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
        // this.schedule = [];
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
.schedule {
  font-family: "Roboto Mono";
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}
.table {
  max-height: 300px;
  overflow: auto;
}
.years {
  margin-right: 1rem;
}
.loading {
  padding-left: 4rem;
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
::-webkit-scrollbar {
    display: none;
}
</style>

<template>
  <h2 id="title">Schedule for {{ season }} Formula One Season</h2>
  <div class="schedule">
    <div class="years">
      <select @change="onSubmitYear($event)">
        <option v-for="n in 74" :value="2024 - n" :key="2024 - n">{{ 2024 - n }}</option>
      </select>
    </div>
    <div class="table">
      <table>
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
  <!-- Not sure if I want to keep loading animation in. need to find better way maybe -->
  <div class="loading" v-if="load">
    <div></div>
    <div></div>
    <div></div>
  </div>
</template>