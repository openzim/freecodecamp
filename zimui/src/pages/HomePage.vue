<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useMainStore } from '@/stores/main'
import ErrorInfo from '../components/ErrorInfo.vue'

const curriculum = await (await fetch(`content/curriculum/index.json`)).json()

const items = curriculum as { [key: string]: string[] }

const main = useMainStore()
</script>

<template>
  <div class="card centered" v-if="main.locales">
    <div v-for="(superblock, idx) of Object.keys(curriculum)" :key="idx" class="my-2">
      <h1>{{ main.locales[superblock].title }}</h1>
      <!-- eslint-disable-next-line vue/no-v-html-->
      <p v-for="(p, jdx) in main.locales[superblock].intro" :key="jdx" class="my-2" v-html="p"></p>
      <ul>
        <li v-for="item in items[superblock]" :key="item">
          <RouterLink :to="`/${superblock}/${item}`">
            {{ main.locales[superblock].blocks[item].title }}
          </RouterLink>
        </li>
      </ul>
    </div>
  </div>
  <div v-else-if="main.isLoading">Page is loading ...</div>
  <ErrorInfo v-else> Introduction data failed to load. </ErrorInfo>
</template>

<style scoped></style>
