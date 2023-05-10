<!-- By Anthony Ganci -->
<script>
import router from "@/router";
export default {
  data() {
    return {
      season: 2023,
      standings: null,
      fetching: true,
    };
  },
  methods: {
    async fetchStandings() {
      const res = await fetch('http://localhost:3001/standings/2023', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
      })
      const data = await res.json();
      this.standings = data.standings;
      this.fetching = false;
    },
    onSubmitYear(event) {
        this.season = parseInt(event);
        router.push({ path: `/standings/${this.season}`})
    },
  },
  async mounted() {
    await this.fetchStandings();
  },
};
</script>

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

<template>
<div v-if="!fetching">
  <h2 id="title">Standings for {{ season }} Formula One Season</h2>
  <div class="pt-6 flex flex-row justify-center">
    <div>
      <BFormSelect v-model="season" @change="onSubmitYear($event)">
        <BFormSelectOption v-for="n in 74" :value="2024 - n" :key="2024 - n"> {{ 2024-n }}</BFormSelectOption>
      </BFormSelect>
    </div>
    <table class="standings ml-4">
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
