import { createStore } from "vuex";
import type UserCoordinates from "@/interfaces/UserCoordinates";
import { getUserCoordinates, login, register } from "@/http/apiUserCoordinates";
import { LoginForm } from "@/interfaces/LoginForm";

export const DISPATCH_GET_USER_MAP_COORDINATES = "GET_USER_MAP_COORDINATES";
export const DISPATCH_LOGIN = "POST_LOGIN";
export const DISPATCH_REGISTER = "POST_REGISTER";

export const SET_USER_MAP_COORDINATES = "SET_USER_MAP_COORDINATES";
export const SET_TOKEN = "SET_TOKEN";
export const SET_USERNAME = "SET_USERNAME";

interface State {
  userCoordinates: UserCoordinates[];
  username?: string;
  token?: string;
}

const assertHadAuth = (token?: string, username?: string) => {
  if (token === undefined || username === undefined) {
    throw new Error("not authenticated");
  }
};

export default createStore({
  state: {
    userCoordinates: Array<UserCoordinates>(),
    username: undefined,
    token: undefined,
  } as State,
  getters: {},
  mutations: {
    [SET_USER_MAP_COORDINATES]: (
      state: State,
      payload: Array<UserCoordinates>,
    ) => {
      state.userCoordinates = payload;
    },
    [SET_TOKEN]: (state: State, payload: string) => {
      state.token = payload;
    },
    [SET_USERNAME]: (state: State, payload: string) => {
      state.username = payload;
    },
  },
  actions: {
    [DISPATCH_LOGIN]: async ({ commit }, payload: LoginForm) => {
      const token = await login(payload);
      commit(SET_TOKEN, token);
      commit(SET_USERNAME, payload.username);
    },
    [DISPATCH_REGISTER]: async ({ commit }, payload: LoginForm) => {
      const token = await register(payload);
      commit(SET_TOKEN, token);
      commit(SET_USERNAME, payload.username);
    },
    [DISPATCH_GET_USER_MAP_COORDINATES]: async ({ state, commit }) => {
      assertHadAuth(state.token, state.username);
      const responsePoints = await getUserCoordinates(
        state.username!,
        state.token!,
      );

      commit(SET_USER_MAP_COORDINATES, responsePoints);
    },
  },
  modules: {},
});
