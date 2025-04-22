import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

class Auth {
  static async login(creds) {
    return api.post('/auth/', creds)
      .then((resp) => resp.data)
      .catch((err) => {
        throw err;
      });
  }

  static async register(payload) {
    return api.post('/auth/register', payload)
      .then((resp) => resp.data);
  }

  static async restore(payload) {
    return api.post('/auth/restore', payload)
      .then((resp) => resp.data);
  }

  static async refresh(rsfhToken) {
    return api.post('/auth/refresh', {}, { headers: { Authorization: `Bearer ${rsfhToken}` } })
      .then((resp) => resp.data);
  }
}

export default Auth;
