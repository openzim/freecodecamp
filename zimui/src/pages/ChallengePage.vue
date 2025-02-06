<script setup lang="ts">
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import ErrorInfo from '@/components/ErrorInfo.vue'
import ChallengeBreadcrumbs from '@/components/challenge/ChallengeBreadcrumbs.vue'
import ChallengeMobile from '@/components/challenge/ChallengeMobile.vue'
import ChallengeDesktop from '@/components/challenge/ChallengeDesktop.vue'
import { useMainStore } from '@/stores/main'
import { singlePathParam } from '@/utils/pathParams'
import { supportedChallengeTypes } from '@/constants'
import { useDisplay } from 'vuetify'

const main = useMainStore()
const route = useRoute()

const superblock = computed(() => singlePathParam(route.params.superblock))
const course = computed(() => singlePathParam(route.params.course))
const slug = computed(() => singlePathParam(route.params.slug))

const { smAndDown } = useDisplay()

watch(
  () => `${superblock.value}/${course.value}/${slug.value}`,
  async () => {
    await main.fetchChallenge(superblock.value, course.value, slug.value)
  },
  { immediate: true }
)
</script>

<template>
  <div class="page" v-if="main.isLoading">Page is loading ...</div>
  <div class="page" v-else-if="main.challenge && main.localesIntro">
    <ChallengeBreadcrumbs />
    <div
      v-if="supportedChallengeTypes.includes(main.challenge.header['challengeType'])"
      class="challenge"
    >
      <ChallengeMobile v-if="smAndDown" />
      <ChallengeDesktop v-else />
    </div>
    <ErrorInfo v-else> This type of challenge is not yet working offline. </ErrorInfo>
  </div>
  <ErrorInfo class="page" v-else> Challenge not found. </ErrorInfo>
</template>

<style scoped>
.page {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.challenge {
  flex: 1 1 auto;
  min-height: 0;
}
</style>
