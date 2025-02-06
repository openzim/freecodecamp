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
</script>

<template>
  <div v-if="main.localesTranslations" class="main">
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
        {{ main.localesTranslations.buttons['reset-lesson'] }}
      </button>
      <button @click="main.runTest()">{{ main.localesTranslations.buttons['run'] }}</button>

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
  background-color: #3b3b4f;
  color: #fff;
}

.header {
  border-bottom: 1px solid #3b3b4f;
}

.footer > button {
  background-color: #d0d0d5;
  color: #1b1b32;
  border: 3px solid #1b1b32;
}

.footer {
  border-top: 1px solid #fff;
}

.code-editor {
  background-color: #fff;
}
</style>
