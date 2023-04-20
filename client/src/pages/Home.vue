<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import curriculum from '../assets/curriculum/index.json'
import { titleize } from '../utils/titleize'

const router = useRouter()

router.push('/english/basic-javascript')
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
