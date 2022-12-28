<!-- This basic placeholder template for the Standings webpage was developed by Colin Martires -->

<template>
  <h1>Standings</h1>
  <table>
    <thead>
      <tr>
        <th>Standing</th>
        <th>Name</th>
        <th>Points</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(driver, index) in drivers" :key="index">
        <td>{{driver[0]}}</td>
        <td>{{driver[1]}}</td>
        <td>{{driver[2]}}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import axios from "axios";
export default {
  name: "Standings",
  data() {
    return {
      drivers: []
    }
  },
  methods: {
    getStandingsData() {
      const path = "http://localhost:5000/standings";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.drivers = res.data.drivers;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.getStandingsData();
  }
};
</script>

<style></style>
