<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import ErrorInfo from '../components/ErrorInfo.vue'
import { RouterLink } from 'vue-router'
import { computed } from 'vue'
import SuperblockIcon from './SuperblockIcon.vue'

import right_arrow from '../assets/right_arrow.svg'

const main = useMainStore()

const randomQuote = computed(() => {
  return main.localesMotivation?.motivationalQuotes.random()
})
</script>

<template>
  <div
    v-if="
      main.curriculums && main.localesIntro && main.localesMotivation && main.localesTranslations
    "
  >
    <h1>{{ main.localesTranslations.learn['heading'] }}</h1>
    <blockquote>
      <q>{{ randomQuote?.quote }}</q>
      <footer>
        <cite>{{ randomQuote?.author }}</cite>
      </footer>
    </blockquote>
    <ul>
      <li v-for="curriculum in Object.keys(main.curriculums)" :key="curriculum">
        <RouterLink :to="`/${curriculum}`">
          <div class="course">
            <SuperblockIcon :superblock="curriculum" class="icon" />
            <span>{{ main.localesIntro[curriculum].title }}</span>
            <img :src="right_arrow" aria-hidden="true" />
          </div>
        </RouterLink>
      </li>
    </ul>
  </div>
  <ErrorInfo v-else>Insufficient data loaded for CurriculumOverview</ErrorInfo>
</template>

<style scoped>
div.course {
  display: flex;
  align-items: center;
  gap: 15px;
  background-color: #d0d0d5;
  border: 3px solid #1b1b32;
  color: #1b1b32;
  font-size: 1.1rem;
  margin-bottom: 10px;
  min-height: 80px;
  padding: 0.625rem 1rem;
}

div.course span {
  flex-grow: 1;
}

h1 {
  margin: 30px 0;
  font-weight: bold;
  font-size: 1.5rem;
  text-align: center;
}

blockquote {
  font-size: 1.3rem;
  margin: 0 0 20px;
  padding: 10px 20px;
  text-align: center;
}

footer:before {
  content: '\2014 \00A0';
}

.icon {
  width: 45px;
}

ul {
  margin: 0 90px;
}

@media (max-width: 1024px) {
  ul {
    margin: 0;
  }
}

@media (max-width: 700px) {
  div.course {
    font-size: 1rem;
  }
  .icon {
    width: 36px;
  }
}

@media (max-width: 500px) {
  h1 {
    font-size: 1.3rem;
  }
  blockquote {
    font-size: 1.2rem;
  }
}
</style>
