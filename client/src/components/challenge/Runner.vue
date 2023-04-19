<script setup lang="ts">
import { Ref, ref } from 'vue'
import { Challenge } from '@/utils/parseChallenge'
import { runChallenge } from '@/utils/runChallenge'

const props = defineProps<{
  challenge: Challenge
  solution: string
}>()

const emit = defineEmits<{
  (e: 'reset'): void
}>()

type State = 'initialized' | 'passed' | 'error'
const state: Ref<State> = ref('initialized')

const error: Ref<string | null> = ref(null)


const test = (): void => {
  try {
    runChallenge(props.challenge, props.solution)
    error.value = null
    state.value = 'passed'
  } catch (e) {
    if (e instanceof Error) {
      error.value = e.message
      state.value = 'error'
    }
  }
}
</script>

<template>
  <button @click="test">Run</button>
  <button @click="emit('reset')">Reset</button>
  <p v-if="error" class="error">
    <b>{{ error }}</b>
  </p>
  <p v-else-if="state === 'passed'" class="passed">
    <b>Passed!</b>
  </p>
</template>

<style scoped>
.error {
  color: rgb(164, 4, 4);
}
.passed {
  color: rgb(39, 190, 39);
}
</style>
