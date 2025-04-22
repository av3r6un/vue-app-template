<template>
  <router-view/>
</template>
<script>
export default {
  name: 'App',
  data() {
    return {};
  },
  methods: {},
  mounted() {
    document.title = this.$route.meta.title;
  },
};
</script>

<style lang="scss">
#app{
  color: white;
  background: #1b1b1b;
}
</style>
