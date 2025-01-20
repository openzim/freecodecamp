<script setup lang="ts">
import type { Ref, ComputedRef } from 'vue'
import { ref, computed, watch, onMounted } from 'vue'
import { Challenge } from '@/utils/parseChallenge'
import type { RunResult } from '@/utils/runChallenge'
import { runChallenge } from '@/utils/runChallenge'
import type { ChallengeInfo } from '@/types/challenges'
import { useMainStore } from '@/stores/main'
import { singlePathParam } from '@/utils/pathParams.ts'
import { useRoute } from 'vue-router'

const main = useMainStore()
const route = useRoute()

const superblock = computed(() => singlePathParam(route.params.superblock))
const course = computed(() => singlePathParam(route.params.course))
const slug = computed(() => singlePathParam(route.params.slug))

const nextChallenge: Ref<ChallengeInfo | undefined> = computed(() => {
  return main.nextChallenge(slug.value)
})

const result: Ref<RunResult | null> = ref(null)

const cheatMode: Ref<boolean> = ref(false)

const passed: ComputedRef<boolean> = computed(() => {
  if (result.value) {
    return result.value.hints.filter((h) => h.passed).length === result.value.hints.length
  }
  return false
})

const runTest = (): void => {
  result.value = runChallenge(main.challenge as Challenge, main.solution)
  main.logs = result.value.logs
}
result.value = runChallenge(main.challenge as Challenge, '')

watch(
  () => main.challenge,
  () => {
    result.value = runChallenge(main.challenge as Challenge, '')
  }
)

onMounted(() => {
  cheatMode.value = localStorage.getItem('cheatMode') == 'true'
})
</script>

<template>
  <button v-if="cheatMode" @click="main.cheatSolution()">Set solution</button>
  <button @click="runTest">Run the tests</button>
  <div v-if="passed" class="passed">
    <p>Passed!</p>
    <p v-if="nextChallenge">
      <router-link :to="`/${superblock}/${course}/${nextChallenge.slug}`">
        <button>Move to next challenge</button>
      </router-link>
    </p>
  </div>
  <button @click="main.resetSolution()">Reset this lesson</button>
  <p v-for="(test, i) in result?.hints" :key="i" class="hint" :class="{ passed: test.passed }">
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
