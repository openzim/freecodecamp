<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import ErrorInfo from '../components/ErrorInfo.vue'
import CourseBlocks from '@/components/CourseBlocks.vue'
import { toRef } from 'vue'
import SuperblockIcon from './SuperblockIcon.vue'

const main = useMainStore()

const props = defineProps<{
  superblock: string
  activeCourse?: string
}>()

const superblock = toRef(props, 'superblock')
const activeCourse = toRef(props, 'activeCourse')
</script>

<template>
  <div class="my-2" v-if="main.localesIntro && main.localesIntroMiscText && main.curriculums">
    <h1>{{ main.localesIntro[superblock].title }}</h1>
    <SuperblockIcon :superblock="superblock" class="icon" />
    <!-- eslint-disable-next-line vue/no-v-html-->
    <p
      v-for="(p, jdx) in main.localesIntro[superblock].intro"
      :key="jdx"
      class="my-2 super-block-intro"
      v-html="p"
    ></p>
    <h2>{{ main.localesIntroMiscText.courses }}</h2>
    <div
      class="block-parent"
      :id="`${superblock}-${course}`"
      v-for="(course, cdx) in Object.keys(main.curriculums[superblock])"
      :key="course"
    >
      <div class="block">
        <h3 class="block-header">{{ main.localesIntro[superblock].blocks[course].title }}</h3>
        <div class="block-description">
          <p
            v-for="(p, jdx) in main.localesIntro[superblock].blocks[course].intro"
            :key="jdx"
            v-html="p"
          ></p>
          {{ main.localesIntro[course] }}
        </div>
        <CourseBlocks
          :superblock="superblock"
          :course="course"
          :is-open="activeCourse ? course == activeCourse : cdx == 0"
        />
      </div>
    </div>
  </div>
  <ErrorInfo v-else>Insufficient data loaded for SuperblockOverview</ErrorInfo>
</template>

<style scoped>
h1,
h2,
h3 {
  overflow-wrap: break-word;
  font-weight: bold;
}

h1,
h2 {
  text-align: center;
  font-size: 2rem;
  padding-top: 60px;
  padding-bottom: 30px;
  margin: 0.6rem 0;
}

h3 {
  font-size: 1.5rem;
  margin: 0 0 0.6rem;
  padding: 25px 15px 10px;
}

.super-block-intro {
  font-size: 1.17rem;
  margin: 0 0 1.2rem;
}

div.block {
  background-color: white;
  margin-bottom: 30px;
}

div.block-description {
  padding: 0 15px 15px;
  font-size: 1.17rem;
  border-bottom: 3px solid #f5f6f7;
}

.icon {
  display: block;
  height: 120px;
  width: 120px;
  margin: 0 auto 30px;
}

.intro-para {
  margin: 0 0 1.2rem;
}

.block-parent {
  scroll-margin-top: 3rem;
}

@media (max-width: 1024px) {
  .icon {
    height: 100px;
    width: 100px;
  }
}

@media (max-width: 768px) {
  .icon {
    height: 80px;
    width: 80px;
  }
}

@media (max-width: 500px) {
  h1 {
    font-size: 1.5rem;
  }
  h2 {
    font-size: 1.35rem;
  }
  h3 {
    font-size: 1.17rem;
  }
  .super-block-intro,
  div.block-description {
    font-size: 1rem;
  }
}
</style>
