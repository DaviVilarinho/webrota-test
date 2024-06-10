<template>
  <map-auth v-if="store.state.hasAuthModal" />
  <template v-else>
    <nav>
      <router-link to="/">Home</router-link>
      |
      <span v-if="hasAuth" class="font-bold text-blue-300 active:text-blue-200 opacity-50"
        @click="store.commit(LOGOUT)">Sair</span>
      <span v-else class="font-bold text-blue-500 active:text-blue-300"
        @click.prevent="store.commit(TOGGLE_AUTH_MODAL)">Entrar/Cadastrar</span>
    </nav>
    <router-view />
  </template>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useStore } from 'vuex';
import MapAuth from '@/components/MapAuth.vue';
import { TOGGLE_AUTH_MODAL, LOGOUT } from '@/store';

const store = useStore();
const hasAuth = computed(() => store.state.token !== undefined);
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
