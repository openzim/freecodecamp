import ChallengePage from './pages/ChallengePage.vue'
import SuperblockPage from './pages/SuperblockPage.vue'
import HomePage from './pages/HomePage.vue'

export const routes = [
  { path: '/', component: HomePage },
  { path: '/:superblock', component: SuperblockPage },
  { path: '/:superblock/:course', component: SuperblockPage },
  { path: '/:superblock/:course/:slug', component: ChallengePage }
]
