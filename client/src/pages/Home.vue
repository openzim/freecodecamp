<script setup lang="ts">
import { RouterLink } from 'vue-router'
import curriculum from '../assets/curriculum/index.json'
import { titleize } from '../utils/titleize'
</script>

<template>
  <ul>
    <li v-for="item in curriculum['english']" :key="item">
      <RouterLink :to="`/english/${item}`">
        {{ titleize(item) }}
      </RouterLink>
    </li>
  </ul>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
