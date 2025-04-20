import { createStore } from 'vuex';
import api from '../services/axios.service';

export default createStore({
  state: {
    accessToken: localStorage.getItem('accsToken') || null,
    refreshToken: localStorage.getItem('rfshToken') || null,
    user: localStorage.getItem('usr') ? JSON.parse(localStorage.getItem('usr')) : null,
    isAuth: false,
  },
  getters: {
    isAuth: (state) => state.isAuth,
    user: (state) => state.user,
  },
  mutations: {
    setTokens(state, { accs, rfsh }) {
      state.accessToken = accs;
      state.refreshToken = rfsh;
      state.isAuth = true
      localStorage.setItem('accsToken', accs);
      localStorage.setItem('rfshToken', rfsh);
    },
    clearSession(state) {
      state.accessToken = null;
      state.refreshToken = null;
      state.user = null;
      state.isAuth = false;
      localStorage.removeItem('accsToken');
      localStorage.removeItem('rfshToken');
      localStorage.removeItem('usr');
    },
    setUser(state, user) {
      state.user = user;
      localStorage.setItem('usr', JSON.stringify(user));
    },
  },
  actions: {
    async login({ commit }, creds) {
      const { data } = await api.post('/auth/login', creds);
      commit('setTokens', data);
    },
    async register(_, payload) {
      await api.post('/auth/register', payload);
    },
    async restorePassword(_, payload) {
      await api.post('/auth/restore', payload);
    },
    async refresh({ state, commit, }) {
      const { data } = await api.post('/auth/refresh', { refresh: state.refreshToken });
      commit('setTokens', { accs: data.accs, rfsh: data.rfsh });
    },
    logout({ commit }) {
      commit('clearSession');
    },
  },
  modules: {
  },
});
