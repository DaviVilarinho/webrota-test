<template>
  <div class="home">
    <UserMap></UserMap>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useStore } from 'vuex';
import UserMap from '@/components/UserMap.vue';
import { DISPATCH_GET_USER_MAP_COORDINATES } from '@/store';

const store = useStore();

onMounted(() => {
  store.dispatch(DISPATCH_GET_USER_MAP_COORDINATES);
});
</script>
