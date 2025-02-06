// eslint.config.mjs
import pluginVue from 'eslint-plugin-vue'
import {
  defineConfigWithVueTs,
  vueTsConfigs,
  configureVueProject
} from '@vue/eslint-config-typescript'

configureVueProject({
  tsSyntaxInTemplates: true,
  scriptLangs: ['ts']
})

export default defineConfigWithVueTs(
  pluginVue.configs['flat/essential'],
  vueTsConfigs.recommendedTypeChecked,
  {
    ignores: ['**/*.js']
  }
)
