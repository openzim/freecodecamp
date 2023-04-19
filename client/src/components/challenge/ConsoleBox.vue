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
  <p v-if="syntaxError" class="syntaxError">
    {{ syntaxError.name }}
    {{ syntaxError.message }}
  </p>
  <p v-for="log, i in logs" v-else :key="i">
    {{ log }}
  </p>
</template>

<style scoped>
.syntaxError {
  color: red;
}

</style>
