<script setup lang="ts">
import { toRef } from 'vue'

const props = defineProps<{
  logs: string[]
  syntaxError?: Error | null
}>()

const logs = toRef(props, 'logs')
const syntaxError = toRef(props, 'syntaxError')
</script>

<template>
  <div class="box">
    <p v-if="syntaxError" class="syntaxError">
      {{ syntaxError.name }}
      {{ syntaxError.message }}
    </p>
    <pre v-for="(log, i) in logs" v-else :key="i"> > {{ log }} </pre>
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
