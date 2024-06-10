<template>
  <div class="items-center flex items-center justify-center flex-col">
    <h2 class="text-teal-700 font-bold">Mapa do Usuário</h2>
    <VMap style="height: 256px; width: 256px" v-if="hasMarkers"
      :center="[markers?.at(0)?.lat ?? 0, markers?.at(0)?.lng ?? 0]" :zoom="15">
      <VMapOsmTileLayer />
      <VMapZoomControl />
      <VMapAttributionControl />
      <template v-for="marker in markers" :key="marker.date">
        <VMapMarker :latlng="[marker.lat, marker.lng]" :icon-size="[32, 42]">
          <VMapDefaultIcon />
        </VMapMarker>
      </template>
    </VMap>
    <p v-else-if="hasToken" class="text-slate-500">
      Não há marcadores ainda, adicione pontos logo abaixo
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import {
  VMap, VMapDefaultIcon, VMapAttributionControl, VMapMarker, VMapOsmTileLayer, VMapZoomControl,
} from 'vue-map-ui';
import { useStore } from 'vuex';
import { DISPATCH_GET_USER_MAP_COORDINATES } from '@/store';

const store = useStore();
const markers = computed(() => store.state.userCoordinates);
const hasMarkers = computed(() => store.state.userCoordinates.length > 0);
const hasToken = computed(() => store.state.token !== undefined);
</script>

<style>
.leaflet-pane.leaflet-shadow-pane {
  display: none;
}
</style>
