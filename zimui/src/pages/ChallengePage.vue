<script setup lang="ts">
import type { Ref } from 'vue'
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import CodeEditor from '../components/challenge/CodeEditor.vue'
import ErrorInfo from '../components/ErrorInfo.vue'
import ChallengeInstructions from '../components/challenge/ChallengeInstructions.vue'
import ChallengeRunner from '../components/challenge/ChallengeRunner.vue'
import { Challenge } from '@/utils/parseChallenge'
import ConsoleLogger from '@/components/challenge/ConsoleLogger.vue'
import { useMainStore } from '@/stores/main'
import { singlePathParam } from '../utils/pathParams.ts'

const main = useMainStore()
const route = useRoute()

const superblock = computed(() => singlePathParam(route.params.superblock))
const course = computed(() => singlePathParam(route.params.course))
const slug = computed(() => singlePathParam(route.params.slug))

const locales = computed(() => (main.locales ? main.locales[superblock.value] : undefined))

const solution: Ref<string> = ref('')
const logs: Ref<string[]> = ref([])

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
    solution.value = main.challenge?.seed || ''
  },
  { immediate: true }
)

const onReset = () => {
  solution.value = main.challenge?.seed || ''
}

const onSetSolution = () => {
  solution.value = main.challenge?.solutions[0] || ''
}
</script>

<template>
  <div v-if="main.challenge && main.locales">
    <div v-if="['1', '4', '5'].includes(main.challenge.header['challengeType'])" class="split">
      <div class="left">
        <ChallengeInstructions
          :title="main.challenge.header['title']"
          :instructions="main.challenge.instructions || ''"
          :description="main.challenge.description"
          :coursetitle="locales.blocks[course].title"
          :coursepath="`/${superblock}/${course}`"
          :curriculumtitle="main.locales[superblock].title"
        ></ChallengeInstructions>
        <ChallengeRunner
          :challenge="main.challenge as Challenge"
          :solution="solution || ''"
          :superblock="superblock"
          :course="course"
          :slug="slug || ''"
          @reset="onReset"
          @set-solution="onSetSolution"
          @logs="(value: any) => (logs = value)"
        ></ChallengeRunner>
      </div>
      <div class="right">
        <CodeEditor
          :source-code="solution"
          class="codeEditor"
          @update="(event: any) => (solution = event)"
        ></CodeEditor>
        <ConsoleLogger class="console" :logs="logs || []"></ConsoleLogger>
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
