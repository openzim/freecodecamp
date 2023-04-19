import Challenge from './pages/Challenge.vue'
import Challenges from './pages/Challenges.vue'
import Home from './pages/Home.vue'

export const routes = [
  { path: '/', component: Home },
  { path: '/:language/:course', component: Challenges },
  { path: '/:language/:course/:slug', component: Challenge },
]
