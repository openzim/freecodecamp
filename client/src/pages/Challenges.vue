<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'

const { params } = useRoute()

const challenges = (
  await import(
    `../assets/curriculum/${params.language}/${params.course}/_meta.json`
  )
).default['challenges']
</script>

<template>
  <ul>
    <li v-for="item in challenges" :key="item.slug">
      <RouterLink :to="`/english/${params.course}/${item.slug}`">
        {{ item.title }}
      </RouterLink>
    </li>
  </ul>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
