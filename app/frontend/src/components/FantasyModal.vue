<script>
export default {
    // props: ['allDrivers', 'buttonTitle', 'title'],
    props: {
      allDrivers: Array,
      buttonTitle: String,
      // forDriver: Number,
    },
    data() {
        return {
            driver1: [],
        }
    },
    methods: {
      load() {
        this.driver1 = [];
      }
    }

}
</script>

<template>
    <!-- Button trigger modal -->
    <button type="button" class="px-6
                  py-2
                  mt-8
                  text-white
                  font-medium
                  text-xl
                  leading-tight
                  rounded
                  hover:bg-slate-400 hover:shadow-lg
                  active:bg-slate-400 active:shadow-lg
                  transition
                  duration-150
                  ease-in-out" data-bs-toggle="modal" data-bs-target="#modal1" @click="load()">
              {{ buttonTitle}}
    </button>
    <!-- Modal -->
    <div class="modal fade fixed top-0 left-0 hidden w-full h-full outline-none overflow-x-hidden overflow-y-auto"
      id="modal1" tabindex="-1" aria-labelledby="modal1Label" aria-hidden="true">
      <div class="modal-dialog relative w-auto pointer-events-none">
        <div
          class="modal-content border-none shadow-lg relative flex flex-col w-full pointer-events-auto bg-slate-700 bg-clip-padding rounded-md outline-none text-current">
          <div
            class="modal-header flex flex-shrink-0 items-center justify-between p-4 border-b border-slate-900 rounded-t-md">
            <h5 class="text-xl font-medium leading-normal" id="modal1Label">Select your first driver:</h5>
            <!-- <h5 class="text-xl font-medium leading-normal" id="modal1Label">{{ forDriver }}</h5> -->
            <button type="button"
              class="btn-close box-content w-4 h-4 p-1 text-black border-none rounded-none opacity-50 focus:shadow-none focus:outline-none focus:opacity-100 hover:text-black hover:opacity-75 hover:no-underline"
              data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body relative p-4">
            <div class="flex flex-col items-start text-xl">
              <!-- <div v-for="(driver, index) in allDrivers" :key="index" @click="$emit('setDriver1', buttonTitle[1], s`driver`)"> {{ driver }}</div> -->
              <div v-for="(driver, index) in allDrivers" :key="index">
                <input type="checkbox" :id="driver.drivername" :value="driver" v-model="driver1">
                <label class="pl-2" :for="driver.drivername">{{ driver.drivername }}</label>
              </div>
            </div>
          </div>
          <div
            class="modal-footer flex flex-shrink-0 flex-wrap items-center justify-end p-4 border-t border-slate-900 rounded-b-md">
            <button type="button" class="px-6
              py-2.5
              bg-purple-600
              text-white
              font-medium
              text-xs
              leading-tight
              uppercase
              rounded
              shadow-md
              hover:bg-purple-700 hover:shadow-lg
              focus:bg-purple-700 focus:shadow-lg focus:outline-none focus:ring-0
              active:bg-purple-800 active:shadow-lg
              transition
              duration-150
              ease-in-out" data-bs-dismiss="modal">Cancel</button>

              <button type="button" class="px-6
              py-2.5
              bg-blue-600
              text-white
              font-medium
              text-xs
              leading-tight
              uppercase
              rounded
              shadow-md
              hover:bg-blue-700 hover:shadow-lg
              focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0
              active:bg-blue-800 active:shadow-lg
              transition
              duration-150
              ease-in-out
              ml-1"
              @click="$emit('setDriver1', driver1[0])"
              data-bs-dismiss="modal"
              >Save</button>
          </div>
        </div>
      </div>
    </div>
</template>