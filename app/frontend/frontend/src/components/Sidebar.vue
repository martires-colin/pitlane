<script>
import SidebarLink from "./SidebarLink.vue";

import { collapsed, toggleSidebar, sidebarWidth } from "./state";
export default {
  props: {},
  components: { SidebarLink },
  setup() {
    return { collapsed, toggleSidebar, sidebarWidth };
  },
};
</script>

<template>
  <div class="sidebar" :style="{ width: sidebarWidth }">
    <h1>
      <span v-if="collapsed">
        <div>
          <img
            src="@/assets/PL.png"
            alt="website logo"
            width="40"
            height="40"
          />
        </div>
      </span>
      <span v-else>
        <div class="logo">
          <img
            src="@/assets/PL.png"
            alt="Website logo"
            width="70"
            height="70"
          />
        </div>
      </span>
    </h1>

    <SidebarLink to="" icon="fas fa-home">Home</SidebarLink>
    <SidebarLink to="" icon="fa-solid fa-ranking-star">Standings</SidebarLink>
    <SidebarLink to="" icon="fa-solid fa-flag-checkered"
      >Fantasy Zone</SidebarLink
    >
    <SidebarLink to="/" icon="fa-solid fa-gears">Settings</SidebarLink>

    <span
      class="collapse-icon"
      :class="{ 'rotate-180': collapsed }"
      @click="toggleSidebar"
    >
      <i class="fa-solid fa-angles-left"></i>
    </span>
  </div>
</template>

<style>
:root {
  --sidebar-bg-color: #222222;
  --sidebar-item-hover: #141414;
  --sidebar-item-active: #000000;
}
</style>
<style scoped>
.sidebar {
  color: #ffffff;
  background-color: var(--sidebar-bg-color);

  float: left;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  bottom: 0;
  padding: 0.5em;

  transition: 0.3s ease;

  display: flex;
  flex-direction: column;
}

.collapse-icon {
  position: absolute;
  bottom: 0;
  padding: 0.75em;

  color: #ffffff;
  transition: 0.2s linear;
}

.rotate-180 {
  transform: rotate(180deg);
  transition: 0.2s linear;
}

.logo {
  position: center;
  bottom: 0;
  padding: 0;
}
</style>
