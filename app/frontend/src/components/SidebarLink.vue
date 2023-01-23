<script>
import { computed } from "vue";
import { useRoute } from "vue-router";
// import { collapsed } from "./state";

export default {
  props: {
    to: { type: String, required: true },
    icon: { type: String, required: true },
  },
  setup(props) {
    const route = useRoute();
    const isActive = computed(() => route.path === props.to);
    // return { isActive, collapsed };
    return { isActive};
  },
};
</script>

<template>
  <div>
    <router-link :to="to" class="link" :class="{ active: isActive }">
      <i class="icon" :class="icon"></i>
      <span class="pl-[12px] hover:text-red-500">
        <slot></slot>
      </span>
      <!-- <Transition name="fade"
        ><span v-if="!collapsed">
          <slot></slot>
        </span>
      </Transition> -->
    </router-link>
  </div>
</template>

<style scoped>
.icon:hover {
  color: #ef4444;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s;
}

.fade-enter-active,
.fade-leave-to {
  opacity: 0;
}
.link {
  display: flex;
  align-items: center;

  cursor: pointer;
  position: relative;
  font-weight: 400;
  user-select: none;

  margin: 0.1em;
  padding: 0.4em;
  border: radius 0.25em;
  height: 1.5em;

  color: #ffffff;
  text-decoration: none;
}

.link:hover {
  background-color: var(--sidebar-item-hover);
}

.link:active {
  background-color: var(--sidebar-item-hover);
}

.link .icon {
  flex-shrink: 0;
  width: 25px;
  margin-right: 10px;
}
</style>
