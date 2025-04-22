<template>
  <article class="home">
    <div class="home_info" v-if="me">{{ me.email }} {{ me.last_ip }} from {{ me.last_device }}</div>
  </article>
</template>

<script>
import Backend from '../services/backend.service';

export default {
  name: 'HomeView',
  data() {
    return {
      api: new Backend(),
      me: null,
    };
  },
  mounted() {
    this.api.get('/auth/me')
      .then((resp) => { this.me = resp; });
  },
};
</script>
