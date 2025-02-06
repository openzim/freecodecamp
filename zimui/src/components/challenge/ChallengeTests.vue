<script setup lang="ts">
import { useMainStore } from '@/stores/main'

import test_failed from '@/assets/test_failed.svg'
import test_passed from '@/assets/test_passed.svg'

const main = useMainStore()
</script>

<template>
  <!--Tests and their results-->
  <h2 class="tests">Tests</h2>
  <ul class="tests">
    <li v-for="(test, i) in main.challengeResult?.hints" :key="i" class="hint">
      <div class="result">
        <img v-if="test.passed" :src="test_passed" />
        <img v-else :src="test_failed" />
      </div>
      {{ i + 1 }}.&nbsp;<span v-html="test.description"></span>
    </li>
  </ul>
</template>

<style>
ul.tests code {
  padding: 1px 4px;
  border: 1px solid #858591;
  background-color: #dfdfe2;
  border-radius: 0;
  color: #2a2a40;
  font-family: 'Hack-ZeroSlash';
  overflow-wrap: anywhere;
  font-size: 1.1rem;
}

ul.tests li:nth-child(2n + 1) code {
  background-color: #f5f6f7;
}
</style>

<style scoped>
.hint {
  align-items: center;
  display: flex;
  line-height: 1.5;
  width: 100%;
  font-size: 1.2rem;
}

.hint .result {
  width: 60px;
  height: 60px;
  align-items: center;
  justify-content: center;
  display: flex;
}

.hint:nth-child(2n + 1) {
  background-color: #dfdfe2;
}

h2.tests {
  text-align: center;
  padding: 0.5rem 0 1rem;
  font-size: 1.1rem;
}
</style>
