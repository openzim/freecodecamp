<script setup lang="ts">
import { computed, ref, toRef } from 'vue'
import { useMainStore } from '@/stores/main'
import block_arrow from '../assets/block_arrow.svg'
import checkbox_empty from '../assets/checkbox_empty.svg'
import checkbox_checked from '../assets/checkbox_checked.svg'
import { RouterLink } from 'vue-router'
import ErrorInfo from '../components/ErrorInfo.vue'

const toggleOpen = () => {
  isOpen.value = !isOpen.value
}

const main = useMainStore()

const props = defineProps<{
  superblock: string
  course: string
  isOpen: boolean
}>()

const superblock = toRef(props, 'superblock')
const course = toRef(props, 'course')

const isOpen = ref(props.isOpen)

const totalChallengesCount = computed(() => {
  return main.curriculums ? main.curriculums[superblock.value][course.value].length : 0
})

const completedChallengesCount = computed(() => {
  // TODO: retrieve amount of completed challenges from local storage
  return 0
})
</script>

<template>
  <button @click="toggleOpen">
    <img :src="block_arrow" class="icon" :class="{ open: isOpen }" aria-hidden="true" />
    <div v-if="isOpen">{{ main.localesIntroMiscText?.collapse }}</div>
    <div v-else>{{ main.localesIntroMiscText?.expand }}</div>
    <div class="completed">
      <img
        :src="completedChallengesCount == totalChallengesCount ? checkbox_checked : checkbox_empty"
        class="icon"
        aria-hidden="true"
      />
      <span aria-hidden="true">{{ completedChallengesCount }}/{{ totalChallengesCount }}</span>
    </div>
  </button>
  <div v-if="main.curriculums">
    <ul class="challenges" v-if="isOpen">
      <li v-for="challenge in main.curriculums[superblock][course]" :key="challenge.slug">
        <RouterLink :to="`/${superblock}/${course}/${challenge.slug}`">
          <img :src="checkbox_empty" aria-hidden="true" />
          {{ challenge.title }}
        </RouterLink>
      </li>
    </ul>
  </div>
  <ErrorInfo v-else>Curriculums are missing</ErrorInfo>
</template>

<style scoped>
button {
  background-color: white;
  width: 100%;
  display: flex;
  gap: 10px;
  border-radius: 0px;
  padding: 18px 15px;
  font-size: 1.13rem;
  border: none;
}

button:hover {
  color: #2a2a40;
  background-color: #dfdfe2;
}

img.icon {
  width: 14px;
}

img.icon.open {
  transform: rotate(90deg);
  -webkit-transform: rotate(90deg);
}

div.completed {
  margin-inline-start: auto;
  padding-inline-end: 5px;
  display: flex;
  gap: 10px;
}

.challenges a {
  padding: 10px 15px;
  width: 100%;
  display: flex;
  gap: 7px;
  text-decoration: none;
  color: inherit;
  font-size: 1.13rem;
}

.challenges a:hover {
  color: #2a2a40;
  background-color: #dfdfe2;
}

@media (max-width: 500px) {
  button,
  .challenges a {
    font-size: 1rem;
  }
}
</style>
