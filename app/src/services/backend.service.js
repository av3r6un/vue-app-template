import api from './axios.service';
import store from '../store';

api.interceptors.request.use(
  (config) => {
    const { headers } = config;
    headers.Authorization = `Bearer ${store.getters.accessToken}`;
    return config;
  },
  (err) => Promise.reject(err),
);

class Backend {
  msg = null;

  extra = null;

  status = 'error';

  manageResp({ data }) {
    let body = null;
    if (data.status === 'success') {
      this.extra = data.extra;
      body = data.body;
    } else {
      this.msg = data.message;
    }
    this.status = data.status;
    return body;
  }

  manageError(data) {
    this.msg = data.msg ? data.msg : '';
    if (data.status === 404) {
      return Promise.reject(data);
    }
    return data;
  }

  async get(url, params) {
    return api.get(url, { params })
      .then((resp) => this.manageResp(resp))
      .catch((err) => this.manageError(err));
  }

  async post(url, data) {
    return api.post(url, { data })
      .then((resp) => this.manageResp(resp))
      .catch((err) => this.manageError(err));
  }
}

export default Backend;
