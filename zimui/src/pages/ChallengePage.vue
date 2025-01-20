<script setup lang="ts">
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import CodeEditor from '../components/challenge/CodeEditor.vue'
import ErrorInfo from '../components/ErrorInfo.vue'
import ChallengeInstructions from '../components/challenge/ChallengeInstructions.vue'
import ChallengeRunner from '../components/challenge/ChallengeRunner.vue'
import ConsoleLogger from '@/components/challenge/ConsoleLogger.vue'
import { useMainStore } from '@/stores/main'
import { singlePathParam } from '../utils/pathParams.ts'

const main = useMainStore()
const route = useRoute()

const superblock = computed(() => singlePathParam(route.params.superblock))
const course = computed(() => singlePathParam(route.params.course))
const slug = computed(() => singlePathParam(route.params.slug))

watch(
  () => `${superblock.value}/${course.value}`,
  () => {
    main.fetchMeta(superblock.value, course.value)
  },
  { immediate: true }
)

watch(
  () => `${superblock.value}/${course.value}/${slug.value}`,
  () => {
    main.fetchChallenge(superblock.value, course.value, slug.value)
  },
  { immediate: true }
)
</script>

<template>
  <div v-if="main.challenge && main.locales">
    <div v-if="['1', '4', '5'].includes(main.challenge.header['challengeType'])" class="split">
      <div class="left">
        <ChallengeInstructions></ChallengeInstructions>
        <ChallengeRunner></ChallengeRunner>
      </div>
      <div class="right">
        <CodeEditor class="codeEditor"></CodeEditor>
        <ConsoleLogger class="console"></ConsoleLogger>
      </div>
    </div>

    <ErrorInfo v-else> This type of challenge is not yet working offline. </ErrorInfo>
  </div>

  <ErrorInfo v-else> Challenge not found. </ErrorInfo>
</template>

<style scoped>
.split {
  @apply flex h-full;
}

.left {
  @apply flex-1 p-8;
}
.right {
  @apply flex-1 flex flex-col;
}
.codeEditor {
  @apply basis-3/4;
}

.console {
  @apply basis-1/4;
}
</style>
