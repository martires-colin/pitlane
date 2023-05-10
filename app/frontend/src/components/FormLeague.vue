<!-- By Anthony Ganci -->

<script>
export default {
    data() {
        return {
            teamInfo: {
                teamname: '',
                owner: '',
                points: '',
            },
            id: this.$route.params.id,
            tid: this.$route.params.tid,
            showNameError: false,
            showPointsError: false,
        }
    },
    methods: {
        triggerNameError() {
          this.showNameError = true;
          setTimeout(() => this.showNameError = false, 2000)
        },
        triggerPointsError() {
          this.showPointsError = true;
          setTimeout(() => this.showPointsError = false, 2000)
        },
        async fetchTeamInfo() {
            const res = await fetch(`http://localhost:3001/fantasy/leagues/${this.$store.state.user.uid}/${this.$route.params.id}?teamname=${this.tid}`, {
                method: 'GET',
                headers: {
                'Content-Type': 'application/json',
                },
                mode: 'cors'
            });
            const data = await res.json();
            console.log(data)
            this.teamInfo = data.teamInfo;
        },
        async updateTeamInfo() {
            if (this.teamInfo.teamname.length > 3) {
              if (this.teamInfo.points >= 0) {
                const res = await fetch(`http://localhost:3001/fantasy/leagues/${this.$store.state.user.uid}/${this.$route.params.id}`, {
                    method: 'PUT',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    mode: 'cors',
                    body: JSON.stringify({'leagueid': this.id, 'teamname': this.tid, 'updatedInfo': this.teamInfo})
                });
                const data = await res.json();
                console.log(data)
                if (data.status == '200') {
                    this.$router.go(-1)
                }
              }
              else {
                this.triggerPointsError();
              }
            }
            else {
              this.triggerNameError();
            }
        },
        
    },
    async mounted() {
        await this.fetchTeamInfo();
    }

}
</script>

<template>
<v-row justify="center">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ tid }}</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="12"
              >
                <v-text-field
                  label="Team name"
                  v-model="teamInfo.teamname"
                  required
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="12"
              >
                <v-text-field
                  label="Owner ID"
                  v-model="teamInfo.owner"
                  disabled
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="12"
              >
                <v-text-field
                  label="Points"
                  v-model="teamInfo.points"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="danger"
            variant="tonal"
            @click="$router.go(-1)"
          >
            Cancel
          </v-btn>
          <v-btn
            color="blue"
            variant="tonal"
            @click="updateTeamInfo"
          >
            Update
          </v-btn>
        </v-card-actions>
      </v-card>
</v-row>
<Teleport to="body">
    <div class="d-flex justify-content-center w-100 fixed-top">
      <transition name="fade">
        <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showNameError">
          Name must be a least 4 characters.
        </div>
      </transition>
    </div>
  </Teleport>
<Teleport to="body">
    <div class="d-flex justify-content-center w-100 fixed-top">
      <transition name="fade">
        <div class="position-absolute top-10 alert alert-danger text-center w-25" role="alert" v-if="showPointsError">
          Points must be at least 0.
        </div>
      </transition>
    </div>
  </Teleport>
</template>