module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/vue3-essential',
    '@vue/airbnb',
  ],
  parserOptions: {
    parser: '@babel/eslint-parser',
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'vuejs-accessibility/click-events-have-key-events': 'off',
    'eslint-plugin-import/no-extraneous-dependencies': 'off',
    'vuejs-accessibility/form-control-has-label': 'off',
    'vuejs-accessibility/anchor-has-content': 'off',
    'vuejs-accessibility/label-has-for': 'off',
    'vuejs-accessibility/no-autofocus': 'off',
    'vue/multi-word-component-names': 'off',
    'vue/multi-word-component-names': 'off',
    'import/no-dynamic-require': 'off',
    'vue/no-v-model-argument': 'off',
    'no-restricted-globals': 'off',
    'no-underscore-dangle': 'off',
    'object-shorthand': 'off',
    'linebreak-style': 'off',
    'global-require': 'off',
  },
};
