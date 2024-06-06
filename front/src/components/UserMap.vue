<template>
  <div class="items-center flex items-center justify-center">
    <VMap style="height: 256px; width: 256px"
      :center="[markers[0].lat, markers[0].lng]"
      :zoom="15" >
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
