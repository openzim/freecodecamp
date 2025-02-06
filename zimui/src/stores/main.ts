import { defineStore } from 'pinia'
import axios, { AxiosError } from 'axios'
import type {
  LocalesIntro,
  LocalesIntroMiscText,
  LocalesMotivation,
  LocalesTranslations
} from '../types/locales'
import type { ChallengeInfo, Curriculums } from '../types/challenges'
import { parseChallenge } from '@/utils/parseChallenge'
import type { Challenge } from '@/utils/parseChallenge'
import mathjaxService from '@/services/mathjax'
import type { RunResult, RunResultHint } from '@/utils/runChallenge'
import { runChallenge } from '@/utils/runChallenge'

export type RootState = {
  localesIntro: LocalesIntro | null
  localesIntroMiscText: LocalesIntroMiscText | null
  localesMotivation: LocalesMotivation | null
  localesTranslations: LocalesTranslations | null
  curriculums: Curriculums | null
  challenge: Challenge | null
  solution: string
  isLoading: boolean
  errorMessage: string
  errorDetails: string
  cheatMode: boolean
  challengeResult: RunResult | null
  challengePassedDialogActive: boolean
  challengeResetDialogActive: boolean
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const nextChallenge = function (state: any) {
  return (
    superblock_slug: string,
    course_slug: string,
    challenge_slug: string
  ): ChallengeInfo | undefined => {
    if (!state.curriculums) {
      return undefined
    }
    const challenges = state.curriculums[superblock_slug][course_slug]
    const challengeIndex = challenges.findIndex((c: ChallengeInfo) => c.slug === challenge_slug)
    if (challengeIndex <= challenges.length) {
      return challenges[challengeIndex + 1]
    }
    return undefined
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const runTest = function (state: any) {
  return (): void => {
    state.challengeResult = runChallenge(state.challenge as Challenge, state.solution)
    if (
      state.challengeResult.hints.filter((h: RunResultHint) => h.passed).length ===
      state.challengeResult.hints.length
    ) {
      state.challengePassedDialogActive = true
    }
  }
}

export const useMainStore = defineStore('main', {
  state: () =>
    ({
      localesIntro: null,
      localesIntroMiscText: null,
      localesMotivation: null,
      localesTranslations: null,
      curriculums: null,
      challenge: null,
      solution: '',
      isLoading: false,
      errorMessage: '',
      errorDetails: '',
      cheatMode: localStorage.getItem('cheatMode') == 'true',
      challengeResult: null,
      challengePassedDialogActive: false,
      challengeResetDialogActive: false
    }) as RootState,
  getters: {
    nextChallenge: nextChallenge,
    runTest: runTest
  },
  actions: {
    async fetchLocalesIntro() {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./content/locales/intro.json').then(
        (response) => {
          this.isLoading = false
          this.localesIntro = response.data as LocalesIntro
          this.localesIntroMiscText = response.data['misc-text'] as LocalesIntroMiscText
        },
        (error) => {
          this.isLoading = false
          this.localesIntro = null
          this.errorMessage = 'Failed to load locales intro.json data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchLocalesMotivation() {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./content/locales/motivation.json').then(
        (response) => {
          this.isLoading = false
          this.localesMotivation = response.data as LocalesMotivation
        },
        (error) => {
          this.isLoading = false
          this.localesMotivation = null
          this.errorMessage = 'Failed to load locales motivation.json data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchLocalesTranslations() {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./content/locales/translations.json').then(
        (response) => {
          this.isLoading = false
          this.localesTranslations = response.data as LocalesTranslations
        },
        (error) => {
          this.isLoading = false
          this.localesTranslations = null
          this.errorMessage = 'Failed to load locales translations.json data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchCurriculums() {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./content/curriculum/index.json').then(
        (response) => {
          this.isLoading = false
          this.curriculums = response.data as Curriculums
        },
        (error) => {
          this.isLoading = false
          this.localesIntro = null
          this.errorMessage = 'Failed to load curriculum/index.json data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchChallenge(superblock: string, course: string, slug: string) {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get(`./content/curriculum/${superblock}/${course}/${slug}.md`).then(
        (response) => {
          this.isLoading = false
          this.challenge = parseChallenge(response.data as string)
          this.resetSolution()
          this.runTest()
          mathjaxService.removeMathJax()
          mathjaxService.addMathJax()
        },
        (error) => {
          this.isLoading = false
          this.challenge = null
          this.errorMessage = `Failed to load challenges markdown for ${superblock}/${course}/${slug}.`
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },

    handleAxiosError(error: AxiosError<object>) {
      if (axios.isAxiosError(error) && error.response) {
        const status = error.response.status
        switch (status) {
          case 400:
            this.errorDetails =
              'HTTP 400: Bad Request. The server could not understand the request.'
            break
          case 404:
            this.errorDetails =
              'HTTP 404: Not Found. The requested resource could not be found on the server.'
            break
          case 500:
            this.errorDetails =
              'HTTP 500: Internal Server Error. The server encountered an unexpected error.'
            break
        }
      }
    },
    setErrorMessage(message: string) {
      this.errorMessage = message
    },
    resetSolution() {
      this.solution = this.challenge?.seed || ''
    },
    cheatSolution() {
      this.solution = this.challenge?.solutions[0] || ''
    }
  }
})
