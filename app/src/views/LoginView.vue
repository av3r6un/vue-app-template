<template>
  <article class="login">
    <form class="login_form" @submit.prevent="logMe">
      <input type="text" required="required" placeholder="Login"
        v-model="userData.username">
      <input type="password" required="required" placeholder="Password"
        v-model="userData.password">
      <button type="submit" class="btn">Войти</button>
    </form>
  </article>
</template>
<script>
export default {
  name: 'Login',
  data() {
    return {
      userData: {
        username: null,
        password: null,
      },
    };
  },
  methods: {
    logMe() {
      this.$store.dispatch('login', this.userData)
        .then((resp) => {
          console.log(resp);
          if (resp) this.$router.push('/');
        });
    },
  },
};
</script>
<style lang="scss" scoped>
.login{
  &_form{
    input{
      display: block;
    }
  }
}
</style>
