<script setup lang="ts">
import { RouteParams, RouterLink, useRoute } from 'vue-router'
import curriculum from '../assets/fcc/index.json'
import { titleize } from '../utils/titleize'
import { Ref, toRef } from 'vue';

const route = useRoute()
const params: Ref<RouteParams> = toRef(route, 'params')

// Assume the first language is our desired langauge unless it's specifically mentioned
// Normally the curriculum index for each zim will only include one language
const language = params.value.language as string || Object.keys(curriculum)[0]
const items = (curriculum as {[key: string]: string[]})[language]

const locales = (
  await import(
    `../assets/fcc/locales/${language}/intro.json`
  )
).default['javascript-algorithms-and-data-structures']

</script>

<template>
  <div class="card centered">
    <h1>{{ locales.title }}</h1>

    <p v-for="(p, idx) in locales.intro" :key="idx" class="my-2">{{ p }}</p>
    <h2 class="mt-8">Courses</h2>
    <ul>
      <li v-for="item in items" :key="item">
        <RouterLink :to="`/${language}/${item}`">
          {{ locales.blocks[item].title }}
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<style scoped>
</style>
