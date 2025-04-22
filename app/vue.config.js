const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: 'dev.vue.home',
    port: 80,
    proxy: {
      '/api/auth': {
        target: 'http://dev.flask.home:48600/auth',
        changeOrigin: true,
        pathRewrite: { '^/api/auth': '' },
      },
      '/api': {
        target: 'http://dev.flask.home:48600/api',
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
      },
    }
  },
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false',
      }),
    ],
  }
});
