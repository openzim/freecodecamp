<script setup lang="ts">
import { ComputedRef, Ref, computed, ref } from 'vue'
import { RouteParams, onBeforeRouteUpdate, useRoute } from 'vue-router'
import CodeEditor from '../components/challenge/CodeEditor.vue'
import Description from '../components/challenge/Description.vue'
import RunnerVue from '../components/challenge/Runner.vue'
import { parseChallenge } from '@/utils/parseChallenge'
import ConsoleBox from '@/components/challenge/ConsoleBox.vue'

export type ChallengeJSON = { title: string; slug: string }
export type ChallengesJSON = {
  challenges: ChallengeJSON[]
}

const { params } = useRoute()
const paramsRef = ref(params)

const markdownChallenge: any = ref(null)
const challenges: Ref<ChallengeJSON[]> = ref([])

challenges.value = (
  (
    await import(
      `../assets/curriculum/${params.language}/${params.course}/_meta.json`
    )
  ).default as ChallengesJSON
)['challenges']

const updateChallenge = async (newparams: RouteParams) => {
  const challenge = await import(
    `../assets/curriculum/${newparams.language}/${newparams.course}/${newparams.slug}.md?raw`
  )
  markdownChallenge.value = challenge.default
}

onBeforeRouteUpdate(async (to) => {
  await updateChallenge(to.params)
  solution.value = challenge.value.seed || ''
  paramsRef.value = to.params
})

const onReset = () => {
  solution.value = challenge.value.seed || ''
}

await updateChallenge(params)

const challenge = computed(() => parseChallenge(markdownChallenge.value))

const nextChallenge: ComputedRef<ChallengeJSON | null> = computed(() => {
  if (!challenge.value) return null
  const challengeIndex = challenges.value.findIndex(
    (c) => c.slug === paramsRef.value.slug
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
      url: `/${paramsRef.value.language}/${paramsRef.value.course}/${nextChallenge.value.slug}`,
    }
  }
  return undefined
})

const solution = ref(challenge.value.seed || '')

const logs: Ref<string[]> = ref([])
</script>

<template>
  <div class="split">
    <div class="left">
      <Description
        :title="challenge.header['title']"
        :instructions="challenge.instructions"
        :description="challenge.description"
      ></Description>
      <RunnerVue
        :challenge="challenge"
        :solution="solution || ''"
        :next-challenge="nextChallengeLink"
        @reset="onReset"
        @logs="(value) => (logs = value)"
      ></RunnerVue>
    </div>
    <div class="right">
      <CodeEditor
        :source-code="solution"
        class="codeEditor"
        @update="(event) => (solution = event)"
      ></CodeEditor>
      <ConsoleBox class="console" :logs="logs || []"></ConsoleBox>
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
