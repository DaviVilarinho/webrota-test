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
    <p v-else-if="hasToken" class="text-slate-500 pb-6">
      Não há marcadores ainda, adicione pontos logo abaixo
    </p>
    <p v-if="hasMarkers" class="pb-6">
      Que legal! Você percorreu <b class="text-2xl">{{ markersDistance.toFixed(0) }}m</b>!
    </p>
    <hr class="w-full pb-6">
    <div v-if="hasToken">
      <div class="mb-3">
        <label class="inline-block mb-2">Latitude</label>
        <input field type="number" name="formUsername"
          class="block w-full py-1.5 px-3 text-gray-800 border border-gray-300 transition duration-500 focus:outline-none focus:border-black rounded"
          placeholder="Latitude" :validate-on-input="true" :value="newLatitude" @input.prevent="changeLat" />
      </div>
      <div class="mb-3">
        <label class="inline-block mb-2">Longitude</label>
        <input field type="number" name="formUsername"
          class="block w-full py-1.5 px-3 text-gray-800 border border-gray-300 transition duration-500 focus:outline-none focus:border-black rounded"
          placeholder="Longitude" :validate-on-input="true" :value="newLongitude" @input.prevent="changeLng" />
      </div>
      <div class="w-full">
        <button type="submit" :disabled="!isFormValid" class="block w-full bg-purple-600 text-white py-1.5 px-3 rounded transition
          hover:bg-purple-700 disabled:bg-slate-300" @click.prevent="newMarker">
          Novo Marcador
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import {
  VMap, VMapDefaultIcon, VMapAttributionControl, VMapMarker, VMapOsmTileLayer, VMapZoomControl,
} from 'vue-map-ui';
import { useStore } from 'vuex';
import { PUT_MARKER } from '@/store';
import type { PutUserCoordinatesForm } from '@/http/apiUserCoordinates';

const store = useStore();
const markers = computed(() => store.state.userCoordinates);
const hasMarkers = computed(() => store.state.userCoordinates.length > 0);
const hasToken = computed(() => store.state.token !== undefined);
const markersDistance = computed(() => store.state.totalDistance);

const newLatitude = ref(0);
const newLongitude = ref(0);

const isLatitudeValid = (lat) => lat <= 90 && lat >= -90;
const isLongitudeValid = (lat) => lat <= 180 && lat >= -180;
const isFormValid = ref(false);
const hasFormError = ref(undefined);

const isLatitudeOrLongitudeInvalid = () => !isLatitudeValid(
  parseFloat(newLatitude.value),
) || !isLongitudeValid(parseFloat(newLongitude.value));

const changeLat = (event) => {
  newLatitude.value = event.target.value;
  isFormValid.value = !isLatitudeOrLongitudeInvalid();
};
const changeLng = (event) => {
  newLongitude.value = event.target.value;
  isFormValid.value = !isLatitudeOrLongitudeInvalid();
};

const isoDateTimezoneSignal = (date: Date, delta: number) => {
  const dateWithTimezone = new Date(date);
  dateWithTimezone.setUTCHours(delta);
  return `${dateWithTimezone.toISOString().slice(0, -1) +
    (delta < 0 ? '-' : '+') +
    (Math.abs(delta) < 10 ? `0${Math.abs(delta.toFixed(1))}` : Math.abs(delta))}:00`;
  // obs não funcionaria para timezone parcial (Venezuela, alguns lugares da China...)
};

const newMarker = async () => {
  if (isFormValid.value) {
    const userDate = new Date();
    try {
      await store.dispatch(PUT_MARKER, {
        date_time: isoDateTimezoneSignal(userDate, userDate.getTimezoneOffset() / 60),
        latitude: parseFloat(newLatitude.value),
        longitude: parseFloat(newLongitude.value),
      } as PutUserCoordinatesForm);
      hasFormError.value = undefined;
    } catch (error) {
      hasFormError.value = "Não foi possível adicionar esta coordenada.";
    }
  }
};

</script>

<style>
.leaflet-pane.leaflet-shadow-pane {
  display: none;
}
</style>
