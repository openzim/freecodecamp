<script setup lang="ts">
import { watch, computed } from 'vue'
import type { RouterLink } from 'vue-router'
import { useRoute } from 'vue-router'
import { useMainStore } from '@/stores/main'
import { singlePathParam } from '../utils/pathParams.ts'
import ErrorInfo from '../components/ErrorInfo.vue'

const main = useMainStore()
const route = useRoute()

const superblock = computed(() => singlePathParam(route.params.superblock))
const course = computed(() => singlePathParam(route.params.course))

const locales = computed(() => (main.locales ? main.locales[superblock.value] : undefined))

watch(
  () => `${superblock.value}/${course.value}`,
  () => {
    main.fetchMeta(superblock.value, course.value)
  },
  { immediate: true }
)
</script>

<template>
  <div v-if="locales && main.challengesMeta" class="card centered">
    <h1>{{ locales.blocks[course].title }}</h1>
    <p>
      <RouterLink :to="`/`"> &gt; {{ locales.title }} </RouterLink>
    </p>
    <!-- eslint-disable-next-line vue/no-v-html-->
    <p v-for="(p, idx) in locales.intro" :key="idx" class="my-2" v-html="p"></p>
    <ul>
      <li v-for="item in main.challengesMeta?.challenges" :key="item.slug">
        <RouterLink :to="`/${superblock}/${course}/${item.slug}`">
          {{ item.title }}
        </RouterLink>
      </li>
    </ul>
  </div>
  <ErrorInfo v-else> Introduction or course data failed to load. </ErrorInfo>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
