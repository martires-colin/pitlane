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
            <p class="pt-[60px] text-xl">+</p>
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
          <!-- <div class="flex flex-row justify-evenly items-center py-1">
            <div>Drivers</div>
            <div>Constructors</div>
          </div> -->
          <!-- <div class="grid grid-cols-2 grid-rows-[20px 20px 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr] h-full"> -->
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