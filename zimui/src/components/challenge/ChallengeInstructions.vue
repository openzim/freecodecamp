<script setup lang="ts">
import { marked } from 'marked'

const props = defineProps<{
  title: string
  description: string
  instructions: string
  coursetitle: string
  coursepath: string
  curriculumtitle: string
}>()

const render = (str: string): string => {
  return marked.parse(str)
}
</script>

<template>
  <!-- eslint-disable vue/no-v-html -->
  <h1>{{ props.title }}</h1>
  <p>
    <RouterLink to="/">
      &gt; {{ curriculumtitle }}
    </RouterLink>
    <RouterLink :to="coursepath">
      &gt; {{ coursetitle }}
    </RouterLink>
  </p>
  <div class="markdown">
    <div v-html="render(props.description)" />
    <hr />
    <div class="instructions" v-html="render(props.instructions)" />
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
