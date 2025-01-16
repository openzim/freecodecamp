import ChallengePage from './pages/ChallengePage.vue'
import ChallengesPage from './pages/ChallengesPage.vue'
import HomePage from './pages/HomePage.vue'

export const routes = [
  { path: '/', component: HomePage },
  { path: '/:superblock/:course', component: ChallengesPage },
  { path: '/:superblock/:course/:slug', component: ChallengePage }
]
