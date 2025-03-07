<script setup lang="ts">
import { marked } from 'marked'
import { useMainStore } from '@/stores/main'

const main = useMainStore()

const render = (str: string): string => {
  return marked.parse(str) as string
}
</script>

<template>
  <div class="instruction-panel">
    <h1>{{ main.challenge?.header['title'] }}</h1>
    <div class="markdown">
      <div class="description" v-html="render(main.challenge?.description || '')"></div>
      <hr v-if="main.challenge?.description && main.challenge?.instructions" />
      <div class="instructions" v-html="render(main.challenge?.instructions || '')"></div>
    </div>
  </div>
</template>

<style>
div.markdown {
  font-size: 1.1rem;
}

div.markdown p {
  line-height: 1.5rem;
  margin: 0 0 1.2rem;
}

div.markdown p:last-child {
  margin: 0;
}

div.markdown code {
  padding: 1px 4px;
  border: 1px solid #858591;
  background-color: #dfdfe2;
  border-radius: 0;
  color: #2a2a40;
  font-family: 'Hack-ZeroSlash';
  overflow-wrap: anywhere;
  font-size: 1.1rem;
}

div.markdown strong {
  font-weight: 700;
  color: #1b1b32;
}

div.markdown hr {
  border: 0;
  border-top: 1px solid #d0d0d5;
  margin-bottom: 20px;
  margin-top: 20px;
}
</style>

<style scoped>
h1 {
  text-align: center;
  font-size: 16px;
  margin: 20px 0 15px;
  min-width: 25px;
  overflow: hidden;
  padding: 0 3px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.instruction-panel {
  padding: 0 10px;
}
</style>
