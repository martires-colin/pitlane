const { defineConfig } = require("@vue/cli-service");
const Components = require('unplugin-vue-components/webpack');
const BootstrapVue3Resolver = require('unplugin-vue-components/resolvers');

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      Components({
        dirs: [
          '.src/components',
          '../node_modules/bootstrap-vue-3/dist/components'
        ],
        resolvers: BootstrapVue3Resolver,
      }),
    ],
  },
});
