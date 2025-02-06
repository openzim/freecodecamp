import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHashHistory } from 'vue-router'
import 'splitpanes/dist/splitpanes.css'
import './style.css'
import App from './App.vue'
import { routes } from './routes'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const app = createApp(App)

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
  scrollBehavior(to) {
    if (to.matched && to.matched[0].path == '/:superblock/:course') {
      return // Scroll is handled inside the page
    }
    return { top: 0, behavior: 'smooth' }
  }
})

app.use(router)

const vuetify = createVuetify({
  components,
  directives,
  display: {
    mobileBreakpoint: 'sm',
    thresholds: {
      xs: 500,
      sm: 768,
      md: 1024,
      lg: 1280,
      xl: 1920
    }
  }
})
app.use(vuetify)

app.use(createPinia())

app.mount('#app')

// declare that we have a new random util function on arrays
declare global {
  interface Array<T> {
    random(): T
  }
}

// and implement it
Array.prototype.random = function () {
  return this[Math.floor(Math.random() * this.length)]
}
