<template>
  <div class="items-center flex items-center justify-center">
    <VMap style="height: 256px; width: 256px"
      :center="[markers?.at(0)?.lat ?? 0, markers?.at(0)?.lng ?? 0]"
      :zoom="15" >
      <VMapOsmTileLayer />
      <VMapZoomControl />
      <VMapAttributionControl />
      <template
          v-for="marker in markers"
          :key="marker.date">
        <VMapMarker
          :latlng="[marker.lat, marker.lng]"
          :icon-size="[32, 42]">
          <VMapDefaultIcon/>
        </VMapMarker>
      </template>
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
