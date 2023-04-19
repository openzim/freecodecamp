<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import CodeEditor from '../components/challenge/CodeEditor.vue'
import Description from '../components/challenge/Description.vue'
import RunnerVue from '../components/challenge/Runner.vue'
import { parseChallenge } from '@/utils/parseChallenge'

const { params } = useRoute()

const markdownChallenge = (
  await import(
    `../assets/curriculum/${params.language}/${params.course}/${params.slug}.md?raw`
  )
).default
const challenge = parseChallenge(markdownChallenge)
const solution = ref(challenge.seed || '')

const onReset = () => {
  solution.value = challenge.seed || ''
}
</script>

<template>
  <div class="card">
    <Description
      :title="challenge.header['title']"
      :instructions="challenge.instructions"
      :description="challenge.description"
    ></Description>
    <CodeEditor
      :source-code="solution"
      @update="(event) => (solution = event)"
    ></CodeEditor>
    <RunnerVue
      :challenge="challenge"
      :solution="solution || ''"
      @reset="onReset"
    ></RunnerVue>
  </div>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
