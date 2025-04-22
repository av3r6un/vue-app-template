import { createStore } from 'vuex';
import Auth from '../services/auth.service';

export default createStore({
  state: {
    accessToken: localStorage.getItem('__accsToken') || null,
    refreshToken: localStorage.getItem('__rfshToken') || null,
    user: localStorage.getItem('__usr') ? JSON.parse(localStorage.getItem('__usr')) : null,
    isAuth: Boolean(localStorage.getItem('__usr')),
  },
  getters: {
    isAuth: (state) => state.isAuth,
    user: (state) => state.user,
    accessToken: (state) => state.accessToken,
    refreshToken: (state) => state.refreshToken,
  },
  mutations: {
    setTokens(state, { tokens }) {
      state.accessToken = tokens.accs_token;
      state.refreshToken = tokens.rfsh_token || null;
      state.isAuth = true;
      localStorage.setItem('__accsToken', tokens.accs_token);
      if (tokens.rfsh_token) localStorage.setItem('__rfshToken', tokens.rfsh_token);
    },
    clearSession(state) {
      state.accessToken = null;
      state.refreshToken = null;
      state.user = null;
      state.isAuth = false;
      localStorage.removeItem('__accsToken');
      localStorage.removeItem('__rfshToken');
      localStorage.removeItem('__usr');
    },
    setUser(state, user) {
      state.user = user;
      localStorage.setItem('__usr', JSON.stringify(user));
    },
  },
  actions: {
    async login({ commit }, creds) {
      return Auth.login(creds)
        .then(({ body }) => {
          commit('setTokens', body);
          // eslint-disable-next-line
          delete body.tokens;
          commit('setUser', body);
          return true;
        })
        .catch((err) => err);
    },
    async register(_, payload) {
      await Auth.register(payload);
    },
    async restorePassword(_, payload) {
      await Auth.restore(payload);
    },
    async refresh({ state, commit }) {
      return Auth.refresh(state.refreshToken)
        .then((body) => {
          commit('setTokens', { tokens: { accs_token: body.token } });
          state.isAuth = true;
          return body.token;
        });
    },
    logout({ commit }) {
      commit('clearSession');
    },
  },
  modules: {
  },
});
