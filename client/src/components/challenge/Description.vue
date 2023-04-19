<script setup lang="ts">
import { marked } from 'marked'

const props = defineProps<{
  title: string
  description: string
  instructions: string
}>()

const render = (str: string): string => {
  return marked.parse(str)
}
</script>

<template>
  <!-- eslint-disable vue/no-v-html -->
  <h1>{{ props.title }}</h1>
  <div v-html="render(props.description)" />
  <hr />
  <div v-html="render(props.instructions)" />
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
