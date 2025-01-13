<script setup lang="ts">
import { Ref, ref, ComputedRef, computed, watch, onMounted } from 'vue'
import { Challenge } from '@/utils/parseChallenge'
import { RunResult, runChallenge } from '@/utils/runChallenge'

const props = defineProps<{
  challenge: Challenge
  solution: string
  nextChallenge?: { title: string; url: string }
}>()

const emit = defineEmits<{
  (e: 'reset'): void
  (e: 'setSolution'): void
  (e: 'logs', logs: string[]): void
}>()

const result: Ref<RunResult | null> = ref(null)

const cheatMode: Ref<boolean> = ref(false)

const passed: ComputedRef<boolean> = computed(() => {
  if (result.value) {
    return (
      result.value.hints.filter((h) => h.passed).length ===
      result.value.hints.length
    )
  }
  return false
})

const runTest = (): void => {
  result.value = runChallenge(props.challenge, props.solution)
  emit('logs', result.value.logs)
}
result.value = runChallenge(props.challenge, '')

watch(
  () => props.challenge,
  () => {
    result.value = runChallenge(props.challenge, '')
  }
)

onMounted(() => {
  cheatMode.value = (localStorage.getItem("cheatMode") == "true")
})

</script>

<template>
  <button v-if="cheatMode" @click="emit('setSolution')">Set solution</button>
  <button @click="runTest">Run the tests</button>
  <div v-if="passed" class="passed">
    <p>Passed!</p>
    <p v-if="nextChallenge">
      <router-link :to="nextChallenge.url">
        <button>Move to next challenge</button>
      </router-link>
    </p>
  </div>
  <button @click="emit('reset')">Reset this lesson</button>
  <p
    v-for="(test, i) in result?.hints"
    :key="i"
    class="hint"
    :class="{ passed: test.passed }"
  >
    {{ test.description }}
  </p>
</template>

<style scoped>
button {
  @apply w-full block my-4;
}

.hint {
  @apply my-8 w-full block pl-4 py-4 bg-gray-100;
}

.hint.passed {
  @apply border-green-600 border-s-2;
}
.error {
  color: rgb(164, 4, 4);
}
.passed {
  color: rgb(39, 190, 39);
}
</style>
