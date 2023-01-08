<<<<<<< Updated upstream
<!-- This basic placeholder template for the Standings webpage was developed by Colin Martires -->

<template>
  <h1>Standings</h1>
  <div v-cloak>
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
  </div>
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
      const path = "http://127.0.0.1:5000/standings";
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

<style>
[v-cloak] {
  display: none;
}
</style>
=======
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
>>>>>>> Stashed changes
