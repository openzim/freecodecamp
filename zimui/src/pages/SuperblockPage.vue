<script setup lang="ts">
import SuperblockOverview from '@/components/SuperblockOverview.vue'
import { useMainStore } from '@/stores/main'
import { singlePathParam } from '@/utils/pathParams'
import { computed, nextTick, onMounted, onUpdated, watch } from 'vue'
import { useRoute } from 'vue-router'
import ErrorInfo from '@/components/ErrorInfo.vue'

const main = useMainStore()
const route = useRoute()

const superblock = computed(() => singlePathParam(route.params.superblock))
const course = computed(() => singlePathParam(route.params.course))

const scrollToCourse = () => {
  const courseEl = document.querySelectorAll(`#${superblock.value}-${course.value}`)
  if (courseEl && courseEl.length > 0) {
    courseEl[0].scrollIntoView()
  }
}

onMounted(scrollToCourse) // scroll when component is mounted
onUpdated(scrollToCourse) // and when component is just updated (e.g. URL manipulated)
watch(
  // and when curriculums are loaded (typically on app loading directly from course URL)
  () => main.curriculums,
  async () => {
    await nextTick()
    scrollToCourse()
  }
)
</script>

<template>
  <div class="main" v-if="main.localesIntro && main.localesIntroMiscText && main.curriculums">
    <SuperblockOverview :superblock="superblock" :activeCourse="course" />
  </div>
  <div class="main" v-else-if="main.isLoading">Page is loading ...</div>
  <ErrorInfo v-else> Data failed to load. </ErrorInfo>
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
