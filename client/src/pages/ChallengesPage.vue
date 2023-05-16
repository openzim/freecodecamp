<script setup lang="ts">
import { Ref, toRef } from 'vue';
import { RouteParams, RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const params: Ref<RouteParams> = toRef(route, 'params')

const challenges = (
  await import(
    `../assets/curriculum/${params.value.language}/${params.value.course}/_meta.json`
  )
).default['challenges']
</script>

<template>
  <div class="card">
    <ul>
      <li v-for="item in challenges" :key="item.slug">
        <RouterLink :to="`/english/${params.course}/${item.slug}`">
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
