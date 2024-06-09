<template>
  <div
    v-if="regShowAlert"
    class="text-white text-center font-bold p-5 mb-4"
    :class="regAlertVariant"
  >
    {{ regAlertMessage }}
  </div>
  <vee-form
    :validation-schema="schema"
    @submit="register"
  >
    <!-- username -->
    <div class="mb-3">
      <label class="inline-block mb-2">Nome de Usuário</label>
      <vee-field
        type="text"
        name="username"
        class="block w-full py-1.5 px-3 text-gray-800 border border-gray-300 transition duration-500 focus:outline-none focus:border-black rounded"
        placeholder="Enter username"
      />
      <VeeErrorMessage
        class="text-red-600"
        name="username"
      />
    </div>
    <div class="mb-3">
      <label class="inline-block mb-2">Senha</label>
      <vee-field
        name="password"
        :bails="false"
        :validate-on-input="true"
        v-slot="{ field, errors }"
      >
        <input
          class="block w-full py-1.5 px-3 text-gray-800 border border-gray-300 transition duration-500 focus:outline-none focus:border-black rounded"
          type="password"
          placeholder="Password"
          v-bind="field"
        >
        <div
          v-for="error in errors"
          :key="error"
          class="text-red-600"
        >
          {{ error }}
        </div>
      </vee-field>
    </div>
    <div class="flex flex-row flex-shrink justify-between flex-grow">
      <button
        type="submit"
        :disabled="regInSubmission"
        class="block bg-purple-600 text-white py-1.5 px-3 rounded transition hover:bg-purple-700"
        @click.prevent="register"
      >
        Registrar
      </button>
      <button
        type="submit"
        :disabled="regInSubmission"
        class="block bg-purple-600 text-white py-1.5 px-3 rounded transition hover:bg-purple-700"
        @click.prevent="login"
      >
        Login
      </button>
    </div>
  </vee-form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { DISPATCH_REGISTER, DISPATCH_LOGIN } from "@/store";
import { useStore } from 'vuex';
import type { LoginForm } from '@/interfaces/LoginForm';
import { sha256 } from 'js-sha256';

const store = useStore();

const CREATING_MESSAGE = 'Sua conta está sendo criada...';
const TRY_LOGIN_MESSAGE = 'Logando...';
const BG_CREATING = 'bg-blue-500';

const CREATED_MESSAGE = 'Sua conta foi criada...';
const OK_LOGIN_MESSAGE = 'Logado!';
const BG_CREATED = 'bg-green-500';

const NOT_CREATED_MESSAGE = 'Não foi possível se registrar, tente novamente.';
const NOK_LOGIN_MESSAGE = 'Não foi possível logar, tente novamente.';
const BG_NOT_CREATED = 'bg-red-500';
const schema = ref({
  username: 'required|min:3|max:100|alpha_spaces',
  password: 'required|min:6|max:100',
});
const regInSubmission = ref(false);
const regShowAlert = ref(false);
const regAlertVariant = ref(BG_CREATING);
const regAlertMessage = ref(CREATING_MESSAGE);

const register = async (registrationForm) => {
  regShowAlert.value = true;
  regInSubmission.value = true;
  regAlertVariant.value = BG_CREATING;
  regAlertMessage.value = CREATING_MESSAGE;

  try {
    await store.dispatch(DISPATCH_REGISTER, {
      username: registrationForm.username,
      hashedPassword: sha256(registrationForm.username),
    } as LoginForm);
  } catch (error) {
    regInSubmission.value = false;
    regAlertVariant.value = BG_NOT_CREATED;
    regAlertMessage.value = NOT_CREATED_MESSAGE;
    return;
  }

  regAlertVariant.value = BG_CREATED;
  regAlertMessage.value = CREATED_MESSAGE;

  window.location.reload();
};

const login = async (loginForm) => {
  regShowAlert.value = true;
  regInSubmission.value = true;
  regAlertVariant.value = BG_CREATING;
  regAlertMessage.value = TRY_LOGIN_MESSAGE;

  try {
    await store.dispatch(DISPATCH_LOGIN, {
      username: loginForm.username,
      hashedPassword: sha256(loginForm.username),
    } as LoginForm);
  } catch (error) {
    regInSubmission.value = false;
    regAlertVariant.value = BG_NOT_CREATED;
    regAlertMessage.value = NOK_LOGIN_MESSAGE;
    return;
  }

  regAlertVariant.value = BG_CREATED;
  regAlertMessage.value = OK_LOGIN_MESSAGE;

  window.location.reload();
};
</script>
