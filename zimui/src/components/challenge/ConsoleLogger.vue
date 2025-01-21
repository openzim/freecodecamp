<script setup lang="ts">
import { toRef } from 'vue'
import { useMainStore } from '@/stores/main'

const main = useMainStore()

const props = defineProps<{
  syntaxError?: Error | null
}>()

const syntaxError = toRef(props, 'syntaxError')
</script>

<template>
  <div class="box">
    <p v-if="syntaxError" class="syntaxError">
      {{ syntaxError.name }}
      {{ syntaxError.message }}
    </p>
    <pre v-for="(log, i) in main.logs" v-else :key="i"> > {{ log }} </pre>
  </div>
</template>

<style scoped>
.box {
  @apply border-2 border-s-black p-4 h-full;
}
.syntaxError {
  color: red;
}
</style>
