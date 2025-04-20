import axios from "axios";
import store from "../store";
import router from '../router';

const api = axios.create({
  baseURL: '/api',
});

api.interceptors.request.use((config) => {
  const token = store.state.accessToken;
  // eslint-disable-next-line
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const originalRequest = err.config;
    if (err.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        await store.dispatch('refreshToken');
        return api(originalRequest);
      } catch (e) {
        store.dispatch('logout');
        router.push('/login');
      }
    }
    return Promise.reject(err);
  }
);

export default api;
