<template>
  <div>
    <h1>Welcome to Pitlane 🏎️!</h1>
    <img :src="msg" />
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Pitlane",
  data() {
    return {
      msg: "",
    };
  },
  methods: {
    getResponse() {
      const path = "http://localhost:5000/pitlane";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.msg = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.getResponse();
  },
};
</script>
