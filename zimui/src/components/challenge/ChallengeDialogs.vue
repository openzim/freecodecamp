<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import type { ComputedRef } from 'vue'
import { computed } from 'vue'
import type { ChallengeInfo } from '@/types/challenges'
import { singlePathParam } from '@/utils/pathParams'
import { useRoute, useRouter } from 'vue-router'

import test_passed from '@/assets/test_passed.svg'

const main = useMainStore()
const route = useRoute()
const router = useRouter()

const superblock = computed(() => singlePathParam(route.params.superblock))
const course = computed(() => singlePathParam(route.params.course))
const slug = computed(() => singlePathParam(route.params.slug))

const nextChallenge: ComputedRef<ChallengeInfo | undefined> = computed(() => {
  return main.nextChallenge(superblock.value, course.value, slug.value)
})

const randomCompliment: ComputedRef<string | undefined> = computed(() =>
  main.localesMotivation?.compliments.random()
)
</script>

<template>
  <!--Reset dialog-->
  <v-dialog
    v-if="main.localesTranslations"
    v-model="main.challengeResetDialogActive"
    max-width="500"
  >
    <template v-slot:default>
      <v-sheet class="danger">
        <div class="header">
          <h2>{{ main.localesTranslations.learn['reset'] }}</h2>
          <button class="close" type="button" @click="main.challengeResetDialogActive = false">
            <span class="sr-only">Close</span>
            <span aria-hidden="true">×</span>
          </button>
        </div>
        <div class="message">
          <p>{{ main.localesTranslations.learn['reset-warn'] }}</p>
          <p>
            <em>{{ main.localesTranslations.learn['reset-warn-2'] }}</em>
          </p>
        </div>
        <div>
          <button
            class="reset"
            type="button"
            @click="
              () => {
                main.challengeResetDialogActive = false
                main.resetSolution()
                main.runTest()
              }
            "
          >
            {{ main.localesTranslations.buttons['reset-lesson'] }}
          </button>
        </div>
      </v-sheet>
    </template>
  </v-dialog>

  <!--Passed dialog-->
  <v-dialog
    v-if="main.localesTranslations"
    v-model="main.challengePassedDialogActive"
    max-width="700"
  >
    <template v-slot:default>
      <v-sheet class="passed">
        <div class="header">
          <h2>{{ randomCompliment }}</h2>
          <button class="close" type="button" @click="main.challengePassedDialogActive = false">
            <span class="sr-only">Close</span>
            <span aria-hidden="true">×</span>
          </button>
        </div>
        <div class="message">
          <img class="big_passed" :src="test_passed" />
          <!-- TODO add progress indication -->
        </div>
        <div>
          <button
            class="next"
            type="button"
            @click="
              () => {
                main.challengePassedDialogActive = false
                router.push(
                  nextChallenge
                    ? `/${superblock}/${course}/${nextChallenge.slug}`
                    : `/${superblock}/${course}`
                )
              }
            "
          >
            {{ main.localesTranslations.buttons['go-to-next'] }}
          </button>
        </div>
      </v-sheet>
    </template>
  </v-dialog>
</template>

<style scoped>
.v-sheet {
  text-align: center;
}

.v-sheet > * {
  padding: 15px;
}

.v-sheet p {
  line-height: 1.5rem;
  margin: 0 0 1.2rem;
}

.v-sheet h2 {
  font-size: 1.2rem;
}

.header {
  display: flex;
  align-items: center;
}

.header,
.message {
  border-bottom: 1px solid #1b1b32;
}

.header h2 {
  flex: 1;
}

.header button {
  margin-top: -15px;
  font-size: 28px;
  line-height: 1.2;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.danger {
  color: #850000;
}

.danger .header {
  background-color: #ffadad;
}

.danger button.reset {
  color: #ffadad;
  background-color: #850000;
  font-size: 1.4rem;
  width: 100%;
  padding: 0.625rem 1rem;
  border: 3px solid #ffadad;
}

.passed button.next {
  color: #1b1b32;
  background-color: #d0d0d5;
  font-size: 1.4rem;
  width: 100%;
  padding: 0.625rem 1rem;
  border: 3px solid #1b1b32;
}

.big_passed {
  -webkit-animation: success-icon-animation 0.15s linear 0.1s forwards;
  animation: success-icon-animation 0.15s linear 0.1s forwards;
  opacity: 0;
  -webkit-transform: scale(1.5);
  transform: scale(1.5);
  width: 200px;
  height: 200px;
}
@-webkit-keyframes success-icon-animation {
  to {
    opacity: 1;
    -webkit-transform: scale(1);
    transform: scale(1);
  }
}
@keyframes success-icon-animation {
  to {
    opacity: 1;
    -webkit-transform: scale(1);
    transform: scale(1);
  }
}
</style>
