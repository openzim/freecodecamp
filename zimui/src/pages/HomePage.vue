<script setup lang="ts">
import {  RouterLink, } from 'vue-router'

const curriculum = await (await fetch(`content/curriculum/index.json`)).json()

const items = (curriculum as {[key: string]: string[]})

const locales = (await (await fetch(`content/locales/intro.json`)).json())

</script>

<template>
  <div class="card centered">

    <div v-for="(superblock, idx) of Object.keys(curriculum)" :key="idx" class="my-2">
      <h1>{{ locales[superblock].title }}</h1>
      <p v-for="(p, jdx) in locales[superblock].intro" :key="jdx" class="my-2">{{ p }}</p>
      <ul>
        <li v-for="item in items[superblock]" :key="item">
          <RouterLink :to="`/${superblock}/${item}`">
            {{ locales[superblock].blocks[item].title }}
          </RouterLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
</style>
