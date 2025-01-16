<script setup lang="ts">
import { Ref, toRef } from 'vue';
import { RouteParams, RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const params: Ref<RouteParams> = toRef(route, 'params')

const challenges = (await (await fetch(`content/curriculum/${params.value.superblock}/${params.value.course}/_meta.json`)).json())['challenges']

const locales = (await (await fetch(`content/locales/intro.json`)).json())[params.value.superblock as string]

</script>

<template>
  <div class="card centered">
    <h1>{{ locales.blocks[params.course as string].title }}</h1>
    <p>
      <RouterLink :to="`/`">
        &gt; {{ locales.title }}
      </RouterLink>
    </p>
    <p v-for="(p, idx) in locales.intro" :key="idx" class="my-2">{{ p }}</p>
    <ul>
      <li v-for="item in challenges" :key="item.slug">
        <RouterLink :to="`/${params.superblock}/${params.course}/${item.slug}`">
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
