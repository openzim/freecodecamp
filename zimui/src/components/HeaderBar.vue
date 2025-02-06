<script setup lang="ts">
import { onMounted } from 'vue'
import { useMainStore } from '@/stores/main'
import headerLogo from '@/assets/freecodecamp-header.svg'

// Fetch the home data
const main = useMainStore()
onMounted(async () => {
  try {
    await Promise.all([
      main.fetchLocalesIntro(),
      main.fetchCurriculums(),
      main.fetchLocalesMotivation(),
      main.fetchLocalesTranslations()
    ])
  } catch {
    main.setErrorMessage('An unexpected error occured.')
  }
})
</script>

<template>
  <div class="header-bar">
    <div id="logo">
      <router-link to="/">
        <img id="logo" :src="headerLogo" alt="freeCodeCamp" class="logo" width="auto" height="70" />
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.header-bar {
  background-color: #0a0a23;
}

#logo {
  display: flex;
  justify-content: center;
  padding: 0.25rem;
}

a:after {
  content: none;
}

@media print {
  .header-bar {
    display: none;
  }
}
</style>
