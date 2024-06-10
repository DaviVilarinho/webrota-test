import { createStore } from "vuex";
import type UserCoordinates from "@/interfaces/UserCoordinates";
import { calculateTotalDistance } from "@/interfaces/UserCoordinates";
import { getUserCoordinates, login, register } from "@/http/apiUserCoordinates";
import { LoginForm } from "@/interfaces/LoginForm";

export const DISPATCH_GET_USER_MAP_COORDINATES = "GET_USER_MAP_COORDINATES";
export const DISPATCH_LOGIN = "POST_LOGIN";
export const DISPATCH_REGISTER = "POST_REGISTER";

export const SET_USER_MAP_COORDINATES = "SET_USER_MAP_COORDINATES";
export const SET_TOKEN = "SET_TOKEN";
export const SET_USERNAME = "SET_USERNAME";
export const SET_DISTANCE = "SET_DISTANCE";

export const TOGGLE_AUTH_MODAL = "TOGGLE_AUTH_MODAL";
export const LOGOUT = "LOGOUT";

interface State {
  userCoordinates: UserCoordinates[];
  username?: string;
  token?: string;
  hasAuthModal: boolean;
  totalDistance: number;
}

const assertHadAuth = (token?: string, username?: string) => {
  if (token === undefined || username === undefined) {
    throw new Error("not authenticated");
  }
};

export default createStore({
  state: {
    userCoordinates: Array<UserCoordinates>(),
    hasAuthModal: false,
    username: undefined,
    token: undefined,
    totalDistance: 0,
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
    [TOGGLE_AUTH_MODAL]: (state: State) => {
      state.hasAuthModal = !state.hasAuthModal;
    },
    [LOGOUT]: (state: State) => {
      state.token = undefined;
      state.userCoordinates = [];
      state.username = undefined;
    },
    [SET_DISTANCE]: (state: State) => {
      state.totalDistance = calculateTotalDistance(state.userCoordinates);
    },
  },
  actions: {
    [DISPATCH_LOGIN]: async ({ commit, dispatch }, payload: LoginForm) => {
      const token = await login(payload);
      commit(SET_TOKEN, token);
      commit(SET_USERNAME, payload.username);
      await dispatch(DISPATCH_GET_USER_MAP_COORDINATES);
    },
    [DISPATCH_REGISTER]: async ({ commit, dispatch }, payload: LoginForm) => {
      const token = await register(payload);
      commit(SET_TOKEN, token);
      commit(SET_USERNAME, payload.username);
      await dispatch(DISPATCH_GET_USER_MAP_COORDINATES);
    },
    [DISPATCH_GET_USER_MAP_COORDINATES]: async ({ state, commit }) => {
      assertHadAuth(state.token, state.username);
      const responsePoints = await getUserCoordinates(
        state.username!,
        state.token!,
      );

      commit(SET_USER_MAP_COORDINATES, responsePoints);
      commit(SET_DISTANCE, responsePoints);
    },
  },
  modules: {},
});
