<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import ErrorInfo from '@/components/ErrorInfo.vue'
import SuperblockOverview from '@/components/SuperblockOverview.vue'
import CurriculumsOverview from '@/components/CurriculumsOverview.vue'

const main = useMainStore()
</script>

<template>
  <div class="main" v-if="main.curriculums && main.localesIntro && main.localesIntroMiscText">
    <CurriculumsOverview v-if="Object.keys(main.curriculums).length > 1" />
    <SuperblockOverview :superblock="Object.keys(main.curriculums)[0]" v-else />
  </div>
  <div class="main" v-else-if="main.isLoading">Page is loading ...</div>
  <ErrorInfo v-else> Introduction data failed to load. </ErrorInfo>
</template>

<style scoped>
div.main {
  width: 780px;
  padding-left: 15px;
  padding-right: 15px;
  margin: auto;
}

@media (max-width: 1024px) {
  div.main {
    width: 625px;
  }
}

@media (max-width: 768px) {
  div.main {
    width: 100%;
  }
}
</style>
