<script setup lang="ts">
import { ComputedRef, Ref, computed, ref, toRef, watch } from 'vue'
import { RouteParams, useRoute } from 'vue-router'
import CodeEditor from '../components/challenge/CodeEditor.vue'
import ChallengeInstructions from '../components/challenge/ChallengeInstructions.vue'
import ChallengeRunner from '../components/challenge/ChallengeRunner.vue'
import { parseChallenge } from '@/utils/parseChallenge'
import ConsoleLogger from '@/components/challenge/ConsoleLogger.vue'

export type ChallengeJSON = { title: string; slug: string }
export type ChallengesJSON = {
  challenges: ChallengeJSON[]
}

const route = useRoute()
const params: Ref<RouteParams> = toRef(route, 'params')

const markdownChallenge: Ref<string | null> = ref(null)
const challenges: Ref<ChallengeJSON[]> = ref([])
const challenge = computed(() => parseChallenge(markdownChallenge.value || ''))
const solution = ref(challenge.value.seed || '')
const logs: Ref<string[]> = ref([])

challenges.value = (
  (
    await import(
      `../assets/curriculum/${params.value.language}/${params.value.course}/_meta.json`
    )
  ).default as ChallengesJSON
)['challenges']

const updateChallenge = async (newparams: RouteParams) => {
  const markdownImport = await import(
    `../assets/curriculum/${newparams.language}/${newparams.course}/${newparams.slug}.md?raw`
  )
  markdownChallenge.value = markdownImport.default as string
  solution.value = challenge.value.seed || ''
}

watch(
  () => route.params,
  async (p: RouteParams) => {
    await updateChallenge(p)
  }
)

const onReset = () => {
  solution.value = challenge.value.seed || ''
}



const nextChallenge: ComputedRef<ChallengeJSON | null> = computed(() => {
  if (!challenge.value) return null
  const challengeIndex = challenges.value.findIndex(
    (c) => c.slug === params.value.slug
  )
  if (challengeIndex <= challenges.value.length) {
    return challenges.value[challengeIndex + 1]
  }
  return null
})

const nextChallengeLink: ComputedRef<
  { title: string; url: string } | undefined
> = computed(() => {
  if (nextChallenge.value) {
    return {
      title: nextChallenge.value.title,
      url: `/${params.value.language}/${params.value.course}/${nextChallenge.value.slug}`,
    }
  }
  return undefined
})


await updateChallenge(params.value)
</script>

<template>
  <div class="split">
    <div class="left">
      <ChallengeInstructions
        :title="challenge.header['title']"
        :instructions="challenge.instructions || ''"
        :description="challenge.description"
      ></ChallengeInstructions>
      <ChallengeRunner
        :challenge="challenge"
        :solution="solution || ''"
        :next-challenge="nextChallengeLink"
        @reset="onReset"
        @logs="(value) => (logs = value)"
      ></ChallengeRunner>
    </div>
    <div class="right">
      <CodeEditor
        :source-code="solution"
        class="codeEditor"
        @update="(event) => (solution = event)"
      ></CodeEditor>
      <ConsoleLogger class="console" :logs="logs || []"></ConsoleLogger>
    </div>
  </div>
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
