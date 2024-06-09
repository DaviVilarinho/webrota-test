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
    :initial-values="userData"
  >
    <!-- username -->
    <div class="mb-3">
      <label class="inline-block mb-2">username</label>
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
      <label class="inline-block mb-2">Password</label>
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
    <button
      type="submit"
      :disabled="regInSubmission"
      class="block w-full bg-purple-600 text-white py-1.5 px-3 rounded transition hover:bg-purple-700"
    >
      Submit
    </button>
  </vee-form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { DISPATCH_REGISTER } from "@/store";
import { useStore } from 'vuex';

const store = useStore();

const CREATING_MESSAGE = 'Your account is being created';
const BG_CREATING = 'bg-blue-500';

const CREATED_MESSAGE = 'Success! Your account has been created.';
const BG_CREATED = 'bg-green-500';

const NOT_CREATED_MESSAGE = 'An error occured creating your user... Try submitting again!';
const BG_NOT_CREATED = 'bg-red-500';
const schema = ref({
  username: 'required|min:3|max:100|alpha_spaces',
  password: 'required|min:6|max:100',
  confirm_password: 'required|passwords_match:@password',
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
    await store.dispatch(DISPATCH_REGISTER, registrationForm);
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
</script>
