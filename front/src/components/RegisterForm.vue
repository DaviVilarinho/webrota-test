<template>
  <div v-if="regShowAlert" class="text-white text-center font-bold p-5 mb-4" :class="regAlertVariant">
    {{ regAlertMessage }}
  </div>
  <!-- username -->
  <div class="mb-3">
    <label class="inline-block mb-2">Nome de Usuário</label>
    <input field type="text" name="formUsername"
      class="block w-full py-1.5 px-3 text-gray-800 border border-gray-300 transition duration-500 focus:outline-none focus:border-black rounded"
      placeholder="Digite nome de usuário" :validate-on-input="true" :value="formUsername"
      @input="event => formUsername = event.target.value" />
  </div>
  <div class="mb-3">
    <label class="inline-block mb-2">Senha</label>
    <input name="formPassword"
      class="block w-full py-1.5 px-3 text-gray-800 border border-gray-300 transition duration-500 focus:outline-none focus:border-black rounded"
      type="password" placeholder="Senha" :value="formPassword" @input="event => formPassword = event.target.value" />
  </div>
  <div class="flex flex-row flex-shrink justify-between flex-grow">
    <button type="submit" :disabled="regInSubmission"
      class="block bg-purple-600 text-white py-1.5 px-3 rounded transition hover:bg-purple-700"
      @click.prevent="register">
      Registrar
    </button>
    <button type="submit" :disabled="regInSubmission"
      class="block bg-purple-600 text-white py-1.5 px-3 rounded transition hover:bg-purple-700" @click.prevent="login">
      Login
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { DISPATCH_REGISTER, DISPATCH_LOGIN, TOGGLE_AUTH_MODAL } from "@/store";
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

const regInSubmission = ref(false);
const regShowAlert = ref(false);
const regAlertVariant = ref(BG_CREATING);
const regAlertMessage = ref(CREATING_MESSAGE);

const formUsername = ref('');
const formPassword = ref('');

const validateForm = (form: LoginForm) => {
  if ((form.username?.length ?? 0) < 3) {
    return 0;
  }
  // empty string
  if (form.hashedPassword === 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855') {
    return 0;
  }
  return 1;
};

const register = async () => {
  regShowAlert.value = true;
  regInSubmission.value = true;
  regAlertVariant.value = BG_CREATING;
  regAlertMessage.value = CREATING_MESSAGE;

  try {
    const registerForm = {
      username: formUsername.value,
      hashedPassword: sha256(formPassword.value),
    } as LoginForm;
    if (!validateForm(registerForm)) {
      throw new Error('Invalid registration');
    }
    await store.dispatch(DISPATCH_REGISTER, registerForm);
  } catch (error) {
    regInSubmission.value = false;
    regAlertVariant.value = BG_NOT_CREATED;
    regAlertMessage.value = NOT_CREATED_MESSAGE;
    return;
  }

  regAlertVariant.value = BG_CREATED;
  regAlertMessage.value = CREATED_MESSAGE;

  setTimeout(() => { }, 1000);
  regShowAlert.value = false;

  store.commit(TOGGLE_AUTH_MODAL);
};

const login = async () => {
  regShowAlert.value = true;
  regInSubmission.value = true;
  regAlertVariant.value = BG_CREATING;
  regAlertMessage.value = TRY_LOGIN_MESSAGE;

  try {
    const loginForm = {
      username: formUsername.value,
      hashedPassword: sha256(formPassword.value),
    } as LoginForm;
    await store.dispatch(DISPATCH_LOGIN, loginForm);
  } catch (error) {
    regInSubmission.value = false;
    regAlertVariant.value = BG_NOT_CREATED;
    regAlertMessage.value = NOK_LOGIN_MESSAGE;
    return;
  }

  regAlertVariant.value = BG_CREATED;
  regAlertMessage.value = OK_LOGIN_MESSAGE;

  setTimeout(() => { }, 1000);
  regShowAlert.value = false;

  store.commit(TOGGLE_AUTH_MODAL);
};
</script>
