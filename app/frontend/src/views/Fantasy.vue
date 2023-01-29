<!-- Started by Anthony Ganci -->

<template>
  <div class="flex flex-col h-screen">
    <div class="flex flex-row justify-between p-4">
      <h1>{{ $store.state.user[0]}}'s Fantasy League</h1>
      <h1>Total points: 0</h1>
    </div>
    <div class="flex flex-row justify-evenly px-10 pb-2">
      <div class="flex flex-row">
          <p class="text-red-500 pr-4">Previous Race</p>
          <img :src="$store.state.prevRace[2]" alt="" height="40" width="40"/>
          <p class="px-4">{{ $store.state.prevRace[0] }} </p>
          <p>{{ $store.state.prevRace[1] }} </p>
      </div>
      <div class="flex flex-row">
          <p class="text-green-500 pr-4">Next Race</p>
          <img :src="$store.state.nextRace[2]" alt="" height="40" width="40"/>
          <p class="px-4"> {{ $store.state.nextRace[0] }}</p>
          <p>{{ $store.state.nextRace[1] }} </p>
      </div>
    </div>
    <div class="fantasy-grid">
      <div class="bg-dark-300 flex flex-col justify-evenly">
        <div class="flex flex-row justify-evenly">
          <div class="driver-item">
            <p class="py-2">Add Driver</p>
            <!-- Button trigger modal -->
            <button type="button" class="px-6
                  py-2
                  mt-16
                  text-white
                  font-medium
                  text-xl
                  leading-tight
                  rounded
                  hover:bg-slate-400 hover:shadow-lg
                  active:bg-slate-400 active:shadow-lg
                  transition
                  duration-150
                  ease-in-out" data-bs-toggle="modal" data-bs-target="#exampleModal">
              +
            </button>
            <!-- Modal -->
            <div class="modal fade fixed top-0 left-0 hidden w-full h-full outline-none overflow-x-hidden overflow-y-auto"
              id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
              <div class="modal-dialog relative w-auto pointer-events-none">
                <div
                  class="modal-content border-none shadow-lg relative flex flex-col w-full pointer-events-auto bg-slate-700 bg-clip-padding rounded-md outline-none text-current">
                  <div
                    class="modal-header flex flex-shrink-0 items-center justify-between p-4 border-b border-slate-900 rounded-t-md">
                    <h5 class="text-xl font-medium leading-normal" id="exampleModalLabel">Choose a driver:</h5>
                    <button type="button"
                      class="btn-close box-content w-4 h-4 p-1 text-black border-none rounded-none opacity-50 focus:shadow-none focus:outline-none focus:opacity-100 hover:text-black hover:opacity-75 hover:no-underline"
                      data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body relative p-4">
                    <div class="flex flex-col items-start text-xl">
                      <div v-for="(driver, index) in drivers" :key="index">
                        <input type="checkbox" :name="driver" :value="driver">
                        <label class="pl-2" :for="driver">{{ driver }}</label>
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
                      ml-1">Save changes</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="driver-item">
            <p class="py-2">Add Driver</p>
            <p class="pt-[60px] text-xl">+</p>
          </div>
        </div>
        <div class="flex flex-row justify-center">
          <div class="bg-slate-500 h-32 w-50 rounded-[20px]">
            <p class="py-2">Add Constructor</p>
            <p class="pt-4 text-xl">+</p>
          </div>
        </div>
      </div>
      <div class="bg-sky-900">
        <div class="team-grid py-16">
          <div class="grid-item">Drivers</div>
          <div class="grid-item">Constructors</div>
          <div class="grid-item col-span-2">1</div>
          <div class="grid-item col-span-2">2</div>
          <div class="grid-item col-span-2">3</div>
          <div class="grid-item col-span-2">4</div>
          <div class="grid-item col-span-2">5</div>
          <div class="grid-item col-span-2">6</div>
          <div class="grid-item col-span-2">7</div>
          <div class="grid-item col-span-2">8</div>
          <div class="grid-item col-span-2">9</div>
          <div class="grid-item col-span-2">10</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      drivers: ["Lewis Hamilton", "Charles Leclerc", "Max Verstappen", "George Russell"]
    }
  }
};
</script>

<style>

.driver-item {
  background: slategrey;
  height: 250px;
  width: 200px;
  border-radius: 20px;
}

.fantasy-grid {
  display: grid;
  grid-template-columns: minmax(70%, auto) minmax(auto, 600px);
  grid-template-rows: repeat(1, minmax(0, 1fr));
  height: 100%;
}

.team-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 40px 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
  height: 100%;
}

.grid-item{
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>