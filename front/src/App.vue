<template>
  <nav>
    <router-link to="/">Home</router-link>
    |
    <span
      v-if="hasAuth"
      class="font-bold text-blue-300 active:text-blue-200 opacity-50"
      @click="store.dispatch()"
    >Sair</span>
    <span
      v-else
      class="font-bold text-blue-500 active:text-blue-300"
      @click.prevent="toggleAuthModal"
      @toggle-auth-modal="toggleAuthModal"
    >Entrar/Cadastrar</span>
  </nav>
  <router-view/>
  <map-auth :hidden="!hasAuthModal"/>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useStore } from 'vuex';
import { mapAuth } from '@/components/MapAuth.vue';

const store = useStore();
const hasAuth = computed(() => store.state.token !== undefined);
const hasAuthModal = ref(false);
const toggleAuthModal = () => {
  hasAuthModal.value = !hasAuthModal.value;
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
