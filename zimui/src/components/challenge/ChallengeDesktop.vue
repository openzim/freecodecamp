<script setup lang="ts">
import CodeEditor from '@/components/challenge/CodeEditor.vue'
import ChallengeInstructions from '@/components/challenge/ChallengeInstructions.vue'
import ChallengeTests from '@/components/challenge/ChallengeTests.vue'
import ChallengeDialogs from '@/components/challenge/ChallengeDialogs.vue'
import ConsoleLogger from '@/components/challenge/ConsoleLogger.vue'
import { Splitpanes, Pane } from 'splitpanes'
import { useMainStore } from '@/stores/main'

const main = useMainStore()
</script>

<template>
  <Splitpanes>
    <Pane class="left">
      <ChallengeInstructions />
      <div class="buttons" v-if="main.localesTranslations">
        <!--Cheat button (dev-only)-->
        <button v-if="main.cheatMode" @click="main.cheatSolution()">Set solution</button>

        <!--Run the tests button-->
        <button @click="main.runTest">
          {{ main.localesTranslations.buttons['check-code'] }}
        </button>

        <!--Reset code-->
        <button @click="main.challengeResetDialogActive = true">
          {{ main.localesTranslations.buttons['reset-lesson'] }}
        </button>

        <ChallengeDialogs />

        <ChallengeTests />
      </div>
    </Pane>
    <Pane class="right">
      <Splitpanes horizontal>
        <Pane class="topright" size="70">
          <CodeEditor class="code-editor" />
        </Pane>
        <Pane class="bottomright" size="30">
          <ConsoleLogger />
        </Pane>
      </Splitpanes>
    </Pane>
  </Splitpanes>
</template>

<style scoped>
.left,
.right {
  overflow-y: scroll;
}

.topright {
  display: flex;
  background-color: white;
}

.code-editor {
  width: 100%;
}

.buttons {
  padding: 30px 10px 0;
}

button {
  font-size: 1.2rem;
  width: 100%;
  border: 3px solid #1b1b32;
  background-color: #d0d0d5;
  padding: 0.375rem 0.75rem;
  margin: 0 0 0.5rem;
}
</style>
