<script setup lang="ts">
import { ComputedRef, Ref, computed, ref, toRef, watch } from 'vue'
import { RouteParams, useRoute } from 'vue-router'
import CodeEditor from '../components/challenge/CodeEditor.vue'
import ChallengeInstructions from '../components/challenge/ChallengeInstructions.vue'
import ChallengeRunner from '../components/challenge/ChallengeRunner.vue'
import { parseChallenge } from '@/utils/parseChallenge'
import ConsoleLogger from '@/components/challenge/ConsoleLogger.vue'
import errimageData from '../assets/dead_kiwix.png'

export type ChallengeJSON = { title: string; slug: string }
export type ChallengesJSON = {
  challenges: ChallengeJSON[]
}

const errimage = ref(errimageData)

const route = useRoute()
const params: Ref<RouteParams> = toRef(route, 'params')

const markdownChallenge: Ref<string | null> = ref(null)
const challenges: Ref<ChallengeJSON[]> = ref([])
const challenge = computed(() => parseChallenge(markdownChallenge.value || ''))
const solution = ref(challenge.value.seed || '')
const logs: Ref<string[]> = ref([])

const challengesMeta = await (await fetch(`content/curriculum/${params.value.superblock}/${params.value.course}/_meta.json`)).json()

challenges.value = (challengesMeta as ChallengesJSON)['challenges']

const updateChallenge = async (newparams: RouteParams) => {
  const md = await fetch(`content/curriculum/${newparams.superblock}/${newparams.course}/${newparams.slug}.md`)
  markdownChallenge.value = await md.text()
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
      url: `/${params.value.superblock}/${params.value.course}/${nextChallenge.value.slug}`,
    }
  }
  return undefined
})


await updateChallenge(params.value)
</script>

<template>
  <div v-if="['1', '4', '5'].includes(challenge.header['challengeType'])" class="split">
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

  <div v-else class="unsupported-page">
    <div class="unsupported-container">
      <div class="unsupported-content">
        <p class="unsupported-text">This type of challenge is not yet working offline.</p>
      </div>
      <div class="unsupported-image-container">
        <img :src="errimage" class="unsupported-image" alt="error image" />
      </div>
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

.unsupported-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px;
  text-align: center;
}
.unsupported-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
  margin: 60px 0;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
}
.unsupported-content {
  flex: 1;
  text-align: left;
}
.unsupported-text {
  color: #222;
  margin: 10px 0;
  max-width: 500px;
  line-height: 1.6;
  font-size: 18px;
}
.unsupported-image-container {
  flex: 1;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .unsupported-container {
    flex-direction: column;
    text-align: center;
  }

  .unsupported-text {
    margin: 20px auto;
    font-size: 16px;
  }

  .unsupported-image {
    width: 300px;
  }
}
</style>
