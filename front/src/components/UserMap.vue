<template>
  <div class="flex-1 flex-col items-center">
    <VMap style="height: 256px; width: 256px" :center="[-20,-50]" :zoom="3" >
      <VMapOsmTileLayer />
      <VMapZoomControl />
      <VMapAttributionControl />
      <VMapMarker v-for="marker in markers" :key="marker.date" :latlng="[marker.lat, marker.lng]">
        <VMapDefaultIcon />
      </VMapMarker>
    </VMap>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import {
  VMap, VMapDefaultIcon, VMapAttributionControl, VMapMarker, VMapOsmTileLayer, VMapZoomControl,
} from 'vue-map-ui';
import { useStore } from 'vuex';

const store = useStore();
const markers = computed(() => store.state.userCoordinates);
</script>

<style>
.leaflet-pane.leaflet-shadow-pane {
  display: none;
}
</style>
