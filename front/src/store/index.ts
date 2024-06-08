import { createStore } from 'vuex';
import type UserCoordinates from '@/interfaces/UserCoordinates';

export const DISPATCH_GET_USER_MAP_COORDINATES = 'GET_USER_MAP_COORDINATES';

export default createStore({
  state: {
    userCoordinates: Array<UserCoordinates>(),
  },
  getters: {
  },
  mutations: {
  },
  actions: {
    [DISPATCH_GET_USER_MAP_COORDINATES]: ({ state }) => {
      const responsePoints = [];

      state.userCoordinates = responsePoints.map((apiResponseOneData) => ({
        dateTime: new Date(apiResponseOneData.date_time),
        lat: Number(apiResponseOneData.latitude),
        lng: Number(apiResponseOneData.longitude),
      }));
    },
  },
  modules: {
  },
});
