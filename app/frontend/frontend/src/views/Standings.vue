<script>
import axios from "axios";
export default {
  data() {
    return {
      msg: "Standings",
      standings: [],
    };
  },
  methods: {
    getStandings() {
      const path = "http://127.0.0.1:5000/standings";
      axios.get(path).then((response) => {
        console.log(response);
        if (response.status == 200) {
          this.standings = response.data.drivers;
        }
      });
    },
  },
  created() {
    this.getStandings();
  },
};
</script>

<template>
  <main>
    <h3>{{ msg }}</h3>
    <table>
        <tr>
            <th>Rank</th>
            <th>Driver</th>
            <th>Country</th>
        </tr>
        <tr v-for="(driver, index) in standings" :key="index">
            <td>{{driver[0]}}</td>
          <td>{{driver[1]}}</td>
          <td>{{driver[2]}}</td>
        </tr>
    </table>
  </main>
</template>
