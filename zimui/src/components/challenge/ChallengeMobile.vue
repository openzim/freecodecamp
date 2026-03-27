<script setup lang="ts">
import CodeEditor from '@/components/challenge/CodeEditor.vue'
import ChallengeInstructions from '@/components/challenge/ChallengeInstructions.vue'
import ChallengeTests from '@/components/challenge/ChallengeTests.vue'
import ChallengeDialogs from '@/components/challenge/ChallengeDialogs.vue'
import ConsoleLogger from '@/components/challenge/ConsoleLogger.vue'
import type { Ref } from 'vue'
import { ref } from 'vue'
import { useMainStore } from '@/stores/main'

const main = useMainStore()

enum MobileTab {
  Instructions,
  Code,
  Console
}

const selectedTab: Ref<MobileTab> = ref(MobileTab.Instructions)

function checkCode() {
  main.runTest()
  if (!main.challengePassedDialogActive) {
    main.testsFlash = true
    setTimeout(() => {
      main.testsFlash = false
    }, 900)
  }
}
</script>

<template>
  <div v-if="main.isTranslationsReady" class="main">
    <div class="header">
      <button
        :class="{ active: selectedTab === MobileTab.Instructions }"
        @click="selectedTab = MobileTab.Instructions"
      >
        Instructions
      </button>
      <button
        :class="{ active: selectedTab === MobileTab.Code }"
        @click="selectedTab = MobileTab.Code"
      >
        Code
      </button>
      <button
        :class="{ active: selectedTab === MobileTab.Console }"
        @click="selectedTab = MobileTab.Console"
      >
        Console
      </button>
    </div>
    <div class="content">
      <div v-if="selectedTab === MobileTab.Instructions" class="instructions">
        <ChallengeInstructions />
        <ChallengeTests />
      </div>
      <div v-if="selectedTab === MobileTab.Code" class="code">
        <CodeEditor class="code-editor" />
      </div>
      <div v-if="selectedTab === MobileTab.Console" class="console">
        <ConsoleLogger />
      </div>
    </div>
    <div class="footer">
      <button v-if="main.cheatMode" @click="main.cheatSolution()">Set solution</button>
      <button @click="main.challengeResetDialogActive = true">
        {{ main.t('translations.buttons.reset-lesson') }}
      </button>
      <button :class="{ 'tests-failed-flash': main.testsFlash }" @click="checkCode">
        {{ main.t('translations.buttons.run') }}
      </button>

      <ChallengeDialogs />
    </div>
  </div>
  <ErrorInfo v-else>localesTranslations are missing</ErrorInfo>
</template>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.content {
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: scroll;
}

.header,
.footer {
  flex: 0;
  display: flex;
}

.header > button,
.footer > button {
  flex: 1 1 auto;
  text-align: center;
  padding: 0.375rem 0;
}

.header > button.active {
  background-color: var(--tab-active-background);
  color: var(--tab-active-color);
}

.header {
  border-bottom: 1px solid var(--tab-active-background);
}

.footer > button {
  background-color: var(--button-background);
  color: var(--button-color);
  border: 3px solid var(--foreground-accent);
}

.footer {
  border-top: 1px solid var(--primary-background);
}

.code-editor {
  background-color: var(--editor-background);
}

</style>
