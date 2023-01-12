<!-- This basic placeholder template for the Home webpage was developed by Colin Martires -->

<script>
import Schedule from "../components/ScheduleComp";
import Standings from "../components/StandingsComp";
import axios from 'axios';
export default {
  components: {Schedule, Standings},
  data() {
    return {
      name: "Pitlane",
      message: "",
    }
  },
  methods: {
    getIndex() {
      const path = "http://127.0.0.1:5000/";
      axios.get(path).then((response) => {
        console.log(response);
        if (response.status == 200) {
          this.message = response.data.message;
        }
      });
    }
  },
  created() {
    this.getIndex();
  }
};
</script>

<style scoped lang="scss">
  h1 {
    padding-top: 1rem;
  }
  .landing {
    display: flex;
    flex-direction: row;
    font-family: "Roboto Mono";
  }
  #landing-1 {
    padding-right: 5rem;
    // max-height: 300px;
    // overflow: auto;
  }
  
</style>

<template>
  <h1>{{ name }}</h1>
  <h2>{{ message }}</h2>
  <div class="landing">
    <div id="landing-1" >
      <Schedule/>
    </div>
    <div id="landing-2">
      <Standings/>
    </div>
  </div>
  <!-- <BDropdown id="dropdown-1" text="Dropdown Button">
    <BDropdownItem>{{  }}</BDropdownItem>
  </BDropdown> -->
  <BButton variant="primary">Test</BButton>
</template>