<script setup lang="ts">
import { RouteParams, RouterLink, useRoute } from 'vue-router'
import { Ref, toRef } from 'vue';

const DEFAULT_LANGUAGE = 'english'

const route = useRoute()
const params: Ref<RouteParams> = toRef(route, 'params')
const language = params.value.language as string || DEFAULT_LANGUAGE

const curriculum = await (await fetch(`fcc/curriculum/${language}/index.json`)).json()

// Assume the first language is our desired langauge unless it's specifically mentioned
// Normally the curriculum index for each zim will only include one language
const items = (curriculum as {[key: string]: {[key: string]: string[]}})[language]

const locales = (await (await fetch(`fcc/locales/${language}/intro.json`)).json())

</script>

<template>
  <div class="card centered">

    <div v-for="(superblock, idx) of Object.keys(curriculum[language])" :key="idx" class="my-2">
      <h1>{{ locales[superblock].title }}</h1>
      <p v-for="(p, jdx) in locales[superblock].intro" :key="jdx" class="my-2">{{ p }}</p>
      <h2 class="mt-8">Courses</h2>
      <ul>
        <li v-for="item in items[superblock]" :key="item">
          <RouterLink :to="`/${language}/${superblock}/${item}`">
            {{ locales[superblock].blocks[item].title }}
          </RouterLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
</style>
