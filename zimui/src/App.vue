<script setup lang="ts">
import ErrorInfo from './components/ErrorInfo.vue'
import HeaderBar from './components/HeaderBar.vue'
import { useMainStore } from '@/stores/main'
const main = useMainStore()
</script>

<template>
  <HeaderBar class="header" />
  <div class="content">
    <Suspense>
      <div v-if="main.errorMessage">
        <ErrorInfo>
          <p>{{ main.errorMessage }}</p>
          <p>{{ main.errorDetails }}</p>
        </ErrorInfo>
      </div>
      <router-view v-else></router-view>
    </Suspense>
  </div>
</template>

<style scoped>
.header {
  position: fixed;
  top: 0;
  width: 100%;
  height: 2.2rem;
}

.content {
  position: fixed;
  top: 2.2rem;
  width: 100%;
  height: calc(100vh - 2.2rem);
  overflow-y: scroll;
}

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

:root {
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;

  --bs-body-font-family: var(--bs-font-sans-serif);
  --bs-font-sans-serif: 'Lato';
}

* {
  font-family: 'Lato';
}

@font-face {
  font-family: 'Lato';
  src: url('../content/fonts/lato/Lato-Light.woff') format('woff');
  font-weight: 300;
  font-style: normal;
  font-display: fallback;
}

@font-face {
  font-family: 'Lato';
  src: url('../content/fonts/lato/Lato-Regular.woff') format('woff');
  font-weight: normal;
  font-style: normal;
  font-display: fallback;
}

@font-face {
  font-family: 'Lato';
  src: url('../content/fonts/lato/Lato-Italic.woff') format('woff');
  font-weight: normal;
  font-style: italic;
  font-display: fallback;
}

@font-face {
  font-family: 'Lato';
  src: url('../content/fonts/lato/Lato-Bold.woff') format('woff');
  font-weight: bold;
  font-style: normal;
  font-display: fallback;
}

@font-face {
  font-family: 'Lato';
  src: url('../content/fonts/lato/Lato-Black.woff') format('woff');
  font-weight: 900;
  font-style: normal;
  font-display: fallback;
}

@font-face {
  font-family: 'Hack-ZeroSlash';
  src: url('../content/fonts/Hack-ZeroSlash/Hack-ZeroSlash-Bold.woff') format('woff');
  font-weight: bold;
  font-style: normal;
  font-display: fallback;
}

@font-face {
  font-family: 'Hack-ZeroSlash';
  src: url('../content/fonts/Hack-ZeroSlash/Hack-ZeroSlash-Italic.woff') format('woff');
  font-weight: normal;
  font-style: italic;
  font-display: fallback;
}

@font-face {
  font-family: 'Hack-ZeroSlash';
  src: url('../content/fonts/Hack-ZeroSlash/Hack-ZeroSlash-BoldItalic.woff') format('woff');
  font-weight: bold;
  font-style: italic;
  font-display: fallback;
}

@font-face {
  font-family: 'Hack-ZeroSlash';
  src: url('../content/fonts/Hack-ZeroSlash/Hack-ZeroSlash-Regular.woff') format('woff');
  font-weight: normal;
  font-style: normal;
  font-display: fallback;
}
</style>
