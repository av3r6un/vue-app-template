import axios from 'axios';
import store from '../store';
import router from '../router';

const api = axios.create({
  baseURL: '/api',
});

api.interceptors.request.use((config) => {
  const token = config.url === '/auth/refresh' ? store.getters.refreshToken : store.getters.accessToken;
  const { headers } = config;
  if (token) headers.Authorization = `Bearer ${token}`;
  return config;
});

let isRetry = false;

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const { response, config } = err;
    if (response?.status === 401 && !isRetry) {
      isRetry = true;
      try {
        const newToken = await store.dispatch('refresh');
        if (!newToken) router.push('/auth');
        config.headers.Authorization = `Bearer ${newToken}`;
        return api(config);
      } catch (e) {
        if (e.response.data.msg === 'THE') {
          router.push('/auth');
        }
      }
    }
    return Promise.reject(err);
  },
);

export default api;
