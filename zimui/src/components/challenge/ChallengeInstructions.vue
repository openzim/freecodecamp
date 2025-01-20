<script setup lang="ts">
import { marked } from 'marked'
import { useMainStore } from '@/stores/main'
import { singlePathParam } from '@/utils/pathParams.ts'
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const main = useMainStore()
const route = useRoute()

const superblock = computed(() => singlePathParam(route.params.superblock))
const course = computed(() => singlePathParam(route.params.course))

const render = (str: string): string => {
  return marked.parse(str) as string
}
</script>

<template>
  <h1>{{ main.challenge?.header['title'] }}</h1>
  <p>
    <RouterLink to="/"> &gt; {{ main.locales?.[superblock].title }} </RouterLink>
    <RouterLink :to="`/${superblock}/${course}`">
      &gt; {{ main.locales?.[superblock].blocks[course].title }}
    </RouterLink>
  </p>
  <div class="markdown">
    <div v-html="render(main.challenge?.description || '')"></div>
    <hr />
    <div class="instructions" v-html="render(main.challenge?.instructions || '')"></div>
  </div>
</template>

<style scoped>
hr {
  @apply my-4;
}
h1 {
  @apply mb-4;
}
.instructions {
  @apply pb-4;
}
</style>
