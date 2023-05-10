<!-- By Anthony Ganci -->

<script>
export default {
    props: {
      allConstructors: Array,
      buttonTitle: String,
    },
    data() {
        return {
            constructor1: [],
        }
    },
    methods: {
      load() {
        this.constructor1 = [];
      }
    }

}
</script>

<template>
  <div>
    <!-- Button trigger modal -->
    <button type="button" class="px-6
                  py-2
                  mt-2
                  text-white
                  font-medium
                  text-xl
                  leading-tight
                  rounded
                  hover:bg-slate-400 hover:shadow-lg
                  active:bg-slate-400 active:shadow-lg
                  transition
                  duration-150
                  ease-in-out" data-bs-toggle="modal" data-bs-target="#constructorModal" @click="load()">
              {{ buttonTitle }}
    </button>
    <!-- Modal -->
    <div class="modal fade fixed top-0 left-0 hidden w-full h-full outline-none overflow-x-hidden overflow-y-auto"
      id="constructorModal" tabindex="-1" aria-labelledby="constructorModalLabel" aria-hidden="true">
      <div class="modal-dialog relative w-auto pointer-events-none">
        <div
          class="modal-content border-none shadow-lg relative flex flex-col w-full pointer-events-auto bg-slate-700 bg-clip-padding rounded-md outline-none text-current">
          <div
            class="modal-header flex flex-shrink-0 items-center justify-between p-4 border-b border-slate-900 rounded-t-md">
            <h5 class="text-xl font-medium leading-normal" id="constructorModalLabel">Choose a constructor:</h5>
            <button type="button"
              class="btn-close box-content w-4 h-4 p-1 text-black border-none rounded-none opacity-50 focus:shadow-none focus:outline-none focus:opacity-100 hover:text-black hover:opacity-75 hover:no-underline"
              data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body relative p-4">
            <div class="flex flex-col items-start text-xl">
              <div v-for="(constructor, index) in allConstructors" :key="index">
                <input type="checkbox" :id="constructor" :value="constructor" v-model="constructor1">
                <label class="pl-2" :for="constructor">{{ constructor }}</label>
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
              ease-in-out" data-bs-dismiss="modal">Close</button>
              
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
              @click="$emit('setConstructor', constructor1[0])"
              data-bs-dismiss="modal"
              >Save Constructor</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>