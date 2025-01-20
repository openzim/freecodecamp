<script setup lang="ts">
import ErrorInfo from './components/ErrorInfo.vue'
import HeaderBar from './components/HeaderBar.vue'
import { useMainStore } from '@/stores/main'
const main = useMainStore()
</script>

<template>
  <HeaderBar />
  <Suspense>
    <div v-if="main.errorMessage">
      <ErrorInfo>
        <p>{{ main.errorMessage }}</p>
        <p>{{ main.errorDetails }}</p>
      </ErrorInfo>
    </div>
    <router-view v-else></router-view>
  </Suspense>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
