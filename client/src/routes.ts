import ChallengePage from './pages/ChallengePage.vue'
import ChallengesPage from './pages/ChallengesPage.vue'
import HomePage from './pages/HomePage.vue'

export const routes = [
  { path: '/', component: HomePage },
  { path: '/:language/:course', component: ChallengesPage },
  { path: '/:language/:course/:slug', component: ChallengePage },
]
