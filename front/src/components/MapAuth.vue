<!-- Já possuía um código de autenticação, reaproveitei ele-->
<template>
  <div :class="{
    fixed: true, 'z-10': true, 'overflow-y-auto': true, hidden: !store.state.hasAuthModal,
    'w-full': true
  }" id="modal">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block
      sm:p-0">
      <div class="fixed inset-0 transition-opacity" @click="store.commit(TOGGLE_AUTH_MODAL)">
        <div class="absolute inset-0 bg-gray-800 opacity-75" />
      </div>

      <!-- trick the browser to center the modal -->
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>

      <div
        class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <!-- Add margin if you want to see some of the overlay behind the modal-->
        <div class="py-4 text-left px-6">
          <!--Title-->
          <div class="flex justify-between items-center pb-4">
            <p class="text-2xl font-bold">
              Entrar/Registrar
            </p>
            <!-- Modal Close Button -->
            <span class="modal-close cursor-pointer z-50" @click.prevent="store.commit(TOGGLE_AUTH_MODAL)">
              &nbsp;&nbsp;&nbsp;X&nbsp;&nbsp;&nbsp;
            </span>
          </div>

          <register-form />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import RegisterForm from '@/components/RegisterForm.vue';
import { useStore } from 'vuex';
import { TOGGLE_AUTH_MODAL } from '@/store/index';

const store = useStore();
</script>
