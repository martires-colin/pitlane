<style>
.standings {

}
.years {
  margin-right: 1rem;
}
.standings td {
  border-left: 1px solid;
  border-right: 1px solid;
  border-bottom: 1px solid;
  padding-right: 20px;
  padding-left: 20px;
}
#title {
  padding-top: 1rem;
  padding-bottom: 1rem;
}
#header {
  border-bottom: 1px solid;
}
#driver-name {
  border-right: 1px solid;
  min-width: 150px;
}
#driver-rank {
  border-right: 1px solid;
  min-width: 50px;
}
#driver-points {
  min-width: 50px;
}
#table-driver {
  text-align: left;
}
</style>

<script>
export default {
  data() {
    return {
      standings: [],
      season: this.$route.params.year,
      ready: false,
    }
  },
  methods: {
    async fetchStandings(year) {
        const res = await fetch(`http://localhost:3001/standings/${year}`);
        const data = await res.json();
        console.log(data)
        this.standings = data.standings;
    }
  },
  async mounted() {
    await this.fetchStandings(this.season);
    this.ready = true;
  }
}
</script>

<template>
  <div v-if="ready">
    <h2 id="title">Standings for {{ season }} Formula One Season</h2>
    <RouterLink to="/standings" class="bg-green-500 px-2 rounded-1" >Back</RouterLink>
    <div class="pt-6 flex flex-row justify-center">
      <table class="standings">
          <tr id="header">
              <th id="driver-rank">Rank</th>
              <th id="driver-name">Driver</th>
              <th id="driver-points">Points</th>
          </tr>
          <tr v-for="(driver, index) in standings" :key="index">
              <td>{{driver[0]}}</td>
            <td id="table-driver">{{driver[1]}}</td>
            <td>{{driver[2]}}</td>
          </tr>
      </table>
    </div>
  </div>
</template>
