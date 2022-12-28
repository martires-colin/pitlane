<!-- Data Visualization Page Implemented by Anthony Ganci -->

<template>
  <div class="button-group">
    <button type="button" class="fastf1-button" @click="(show = 1), (src = '')">
      Head-to-Head
    </button>
    <button type="button" class="fastf1-button" @click="(show = 2), (src = '')">
      Gear Shifts
    </button>
    <button type="button" class="fastf1-button" @click="(show = 3), (src = '')">
      Speed Visualization
    </button>
  </div>
  <div class="fastf1">
    <form @submit="onSubmitH2H" v-if="show == 1">
      <div>
        <label>Driver1: </label>
        <input type="text" v-model="form.driver1" placeholder="Driver1" />
      </div>
      <div>
        <label>Driver2: </label>
        <input type="text" v-model="form.driver2" placeholder="Driver2" />
      </div>
      <div>
        <label>Track: </label>
        <select v-model="form.track">
          <option disabled value="">Please select one</option>
          <option>British Grand Prix</option>
          <option>Monaco Grand Prix</option>
          <option>Italian Grand Prix</option>
        </select>
      </div>
      <div>
        <label>Year: </label>
        <input type="text" v-model="form.year" placeholder="Year" />
      </div>
      <div>
        <input type="radio" id="race" value="R" v-model="form.session" />
        <label for="race">Race</label>

        <input type="radio" id="qual" value="Q" v-model="form.session" />
        <label for="qual">Qualifiying</label>
      </div>
      <input type="submit" value="Get Graph" class="btn btn-block" />
    </form>
    <form @submit="onSubmitGear" v-if="show == 2">
      <div>
        <label>Track: </label>
        <!-- <input v-model="gearForm.track" placeholder="Track" /> -->
        <select v-model="gearForm.track">
          <option disabled value="">Please select one</option>
          <option>British Grand Prix</option>
          <option>Monaco Grand Prix</option>
          <option>Italian Grand Prix</option>
        </select>
      </div>
      <div>
        <label>Year: </label>
        <input type="text" v-model="gearForm.year" placeholder="Year" />
      </div>
      <div>
        <input type="radio" id="race" value="R" v-model="gearForm.session" />
        <label for="race">Race</label>

        <input type="radio" id="qual" value="Q" v-model="gearForm.session" />
        <label for="qual">Qualifiying</label>
      </div>
      <input type="submit" value="Get Graph" class="btn btn-block" />
    </form>
    <form @submit="onSubmitSpeedVisual" v-if="show == 3">
      <div>
        <label>Driver: </label>
        <input type="text" v-model="speedForm.driver" placeholder="Driver" />
      </div>
      <div>
        <label>Track: </label>
        <!-- <input v-model="gearForm.track" placeholder="Track" /> -->
        <select v-model="speedForm.track">
          <option disabled value="">Please select one</option>
          <option>British Grand Prix</option>
          <option>Monaco Grand Prix</option>
          <option>Italian Grand Prix</option>
        </select>
      </div>
      <div>
        <label>Year </label>
        <input type="text" v-model="speedForm.year" placeholder="Year" />
      </div>
      <div>
        <input type="radio" id="race" value="R" v-model="speedForm.session" />
        <label for="race">Race</label>

        <input type="radio" id="qual" value="Q" v-model="speedForm.session" />
        <label for="qual">Qualifiying</label>
      </div>
      <input type="submit" value="Get Graph" class="btn btn-block" />
    </form>
  </div>
  <div>
    <div class="loading" v-if="load">
      <div></div>
      <div></div>
      <div></div>
    </div>
    <img style="margin: 10px" :src="src" />
  </div>
</template>

<style lang="scss">
$charade: #282a37;
$bluebell: #979fd0;
$darkish: #133337;
body {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #353839;
}
.button-group {
  padding: 20px;
}
.fastf1-button {
  font-family: "Roboto Mono";
  font-size: 28px;
  text-align: center;
  margin: 5px;
  background-color: #005b96;
  color: #0e1111;
  border-radius: 4px;
  cursor: pointer;
}
.fastf1-button:hover {
  background-color: #03396c;
}
.fastf1 {
  font-family: "Roboto Mono";
  font-size: 20px;
  color: $darkish;
}
.fastf1 input[type="text"],
select {
  font-size: 18px;
}
.fastf1 label {
  text-align: right;
}
.fastf1 input[type="submit"] {
  background-color: #ff2800;
  font-family: "Roboto Mono";
  font-size: 20px;
  border-radius: 4px;
  border-width: 1px;
  margin-top: 8px;
}
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
@keyframes bounce {
  to {
    opacity: 0.3;
    transform: translate3d(0, -1rem, 0);
  }
}
</style>

<script>
import axios from "axios";
export default {
  name: "Pitlane",
  data() {
    return {
      src: "",
      show: 0,
      load: false,
      msg: "",
      form: {
        driver1: "",
        driver2: "",
        track: "",
        year: "",
        session: "",
      },
      gearForm: {
        year: "",
        track: "",
        session: "",
      },
      speedForm: {
        driver: "",
        year: "",
        track: "",
        session: "",
      },
    };
  },
  methods: {
    getPythonData() {
      const path = "http://127.0.0.1:5000/pitlane";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          // this.msg = res.data.msg;
          this.initialFormH2H();
          this.initialFormGear();
          this.initialFormSpeedVisual();
        })
        .catch((err) => {
          console.error(err);
        });
    },
    sendForm(payload) {
      const path = "http://127.0.0.1:5000/pitlane";
      axios
        .post(path, payload)
        .then((res) => {
          this.load = false;
          this.src = res.data.src;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    initialFormH2H() {
      (this.form.driver1 = ""),
        (this.form.driver2 = ""),
        (this.form.track = ""),
        (this.form.session = "R"),
        (this.form.year = "");
    },
    initialFormGear() {
      (this.gearForm.track = ""),
        (this.gearForm.session = "R"),
        (this.gearForm.year = "");
    },
    initialFormSpeedVisual() {
      (this.speedForm.track = ""),
        (this.speedForm.driver = ""),
        (this.speedForm.session = "R"),
        (this.speedForm.year = "");
    },
    onSubmitH2H(e) {
      this.src = "";
      e.preventDefault();
      const payload = {
        method: "headtohead",
        driver1: this.form.driver1,
        driver2: this.form.driver2,
        track: this.form.track,
        session: this.form.session,
        year: this.form.year,
      };
      this.sendForm(payload);
      this.load = true;
      this.initialFormH2H();
    },
    onSubmitGear(e) {
      this.src = "";
      e.preventDefault();
      const payload = {
        method: "gearshift",
        track: this.gearForm.track,
        session: this.gearForm.session,
        year: this.gearForm.year,
      };
      this.sendForm(payload);
      this.load = true;
      this.initialFormGear();
    },
    onSubmitSpeedVisual(e) {
      this.src = "";
      e.preventDefault();
      const payload = {
        method: "speedvisual",
        driver: this.speedForm.driver,
        track: this.speedForm.track,
        session: this.speedForm.session,
        year: this.speedForm.year,
      };
      this.sendForm(payload);
      this.load = true;
      this.initialFormSpeedVisual();
    },
  },
  created() {
    this.getPythonData();
  },
};
</script>