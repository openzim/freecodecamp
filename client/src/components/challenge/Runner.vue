<script setup lang="ts">
import { Ref, ref, ComputedRef, computed} from 'vue'
import { Challenge } from '@/utils/parseChallenge'
import { RunResult, runChallenge } from '@/utils/runChallenge'
import ConsoleBox from './ConsoleBox.vue';

const props = defineProps<{
  challenge: Challenge
  solution: string
}>()

const emit = defineEmits<{
  (e: 'reset'): void
}>()

type State = 'initialized' | 'passed' | 'error'
const state: Ref<State> = ref('initialized')

const error: Ref<Error | null> = ref(null)
const result: Ref<RunResult | null> = ref(null)

const passed: ComputedRef<boolean> = computed(() => {
  if (result.value) {
    return result.value.hints.filter((h) => h.passed).length === result.value.hints.length
  }
  return false
})


const runTest = (): void => {
  try {
    result.value = runChallenge(props.challenge, props.solution)
    error.value = null
  } catch (e) {
    if (e instanceof Error) {
      error.value = e
      state.value = 'error'
    }
  }
}
result.value = runChallenge(props.challenge, props.solution)

</script>

<template>
  <button @click="runTest">Run</button>
  <button @click="emit('reset')">Reset</button>
  <p v-for="test, i in result?.hints" :key="i" class="hint" :class="{ 'passed': test.passed }">{{ test.description }}</p>
  <p v-if="passed" class="passed">
    <b>Passed!</b>
  </p>
  <ConsoleBox :logs="result?.logs || []" :syntax-error="error"></ConsoleBox>
</template>

<style scoped>

.hint {
  margin: 2em;
}

.hint.passed {
}
.error {
  color: rgb(164, 4, 4);
}
.passed {
  color: rgb(39, 190, 39);
}
</style>
