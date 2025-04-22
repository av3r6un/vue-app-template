<template>
  <article class="register">
    <div class="register_title">Регистрация</div>
    <form @submit.prevent="newUser">
      <input type="text" placeholder="username"
        v-model="user.username">
      <input type="password" placeholder="password1"
        v-model="password1">
      <input type="password" placeholder="password2"
        v-model="password2">
      <input type="email" placeholder="email"
        v-model="user.email">
      <button type="submit" class="btn btn_submit">Создать аккаунт</button>
    </form>
  </article>
</template>
<script>
export default {
  name: 'Register',
  data() {
    return {
      user: {
        username: null,
        email: null,
        passwords: [],
      },
      password1: null,
      password2: null,
    };
  },
  methods: {
    newUser() {
      this.user.passwords.push(this.password1);
      this.user.passwords.push(this.password2);
      console.log(this.user);
      this.$store.dispatch('register', this.user)
        .then((resp) => console.log(resp));
    },
  },
  mounted() {
  },
};
</script>
<style lang="scss" scoped>
.register {
  input { display: block; }
}
</style>
