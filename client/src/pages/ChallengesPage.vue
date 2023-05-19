<script setup lang="ts">
import { Ref, toRef } from 'vue';
import { RouteParams, RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const params: Ref<RouteParams> = toRef(route, 'params')

const challenges = (
  await import(
    `../assets/fcc/curriculum/${params.value.language}/${params.value.course}/_meta.json`
  )
).default['challenges']

const locales = (
  await import(
    `../assets/fcc/locales/${params.value.language}/intro.json`
  )
).default['javascript-algorithms-and-data-structures']['blocks'][params.value.course as string]

</script>

<template>
  <div class="card centered">
    <h1>{{ locales.title }}</h1>
    <p v-for="(p, idx) in locales.intro" :key="idx" class="my-2">{{ p }}</p>
    <h2 class="mt-8">Challenges</h2>
    <ul>
      <li v-for="item in challenges" :key="item.slug">
        <RouterLink :to="`/${params.language}/${params.course}/${item.slug}`">
          {{ item.title }}
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
