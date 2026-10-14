import { defineStore } from 'pinia'
import axios, { AxiosError } from 'axios'
import type {
  Config,
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
import { interpolate } from '@/utils/interpolate'

export type RootState = {
  _config: Config | null
  _localesIntro: LocalesIntro | null
  _localesIntroMiscText: LocalesIntroMiscText | null
  _localesMotivation: LocalesMotivation | null
  _localesTranslations: LocalesTranslations | null
  curriculums: Curriculums | null
  challenge: Challenge | null
  solution: string
  isLoading: boolean
  _pendingRequestsCount: number
  errorMessage: string
  errorDetails: string
  cheatMode: boolean
  challengeResult: RunResult | null
  challengePassedDialogActive: boolean
  challengeResetDialogActive: boolean
  testsFlash: boolean
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
  return async (): Promise<void> => {
    state.challengeResult = await runChallenge(state.challenge as Challenge, state.solution)
    if (
      state.challengeResult.hints.filter((h: RunResultHint) => h.passed).length ===
      state.challengeResult.hints.length
    ) {
      state.challengePassedDialogActive = true
    }
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const _useMainStore: any = defineStore('main', {
  state: (): RootState => ({
    _config: null,
    _localesIntro: null,
    _localesIntroMiscText: null,
    _localesMotivation: null,
    _localesTranslations: null,
    curriculums: null,
    challenge: null,
    solution: '',
    // starts true: the first fetches only kick off after the header bar mounts, so
    // defaulting to false would briefly show the "failed to load" fallback on every load
    isLoading: true,
    _pendingRequestsCount: 0,
    errorMessage: '',
    errorDetails: '',
    cheatMode: localStorage.getItem('cheatMode') == 'true',
    challengeResult: null,
    challengePassedDialogActive: false,
    challengeResetDialogActive: false,
    testsFlash: false
  }),
  getters: {
    isIntroReady: (state) => state._localesIntro !== null,
    isIntroMiscTextReady: (state) => state._localesIntroMiscText !== null,
    isMotivationReady: (state) => state._localesMotivation !== null,
    isTranslationsReady: (state) => state._localesTranslations !== null,
    nextChallenge: nextChallenge,
    runTest: runTest
  },
  actions: {
    // tracks concurrently in-flight fetches so isLoading only clears once all of
    // them are done, instead of flipping false as soon as the fastest one resolves
    startLoading() {
      this._pendingRequestsCount += 1
      this.isLoading = true
    },
    stopLoading() {
      this._pendingRequestsCount -= 1
      if (this._pendingRequestsCount <= 0) {
        this._pendingRequestsCount = 0
        this.isLoading = false
      }
    },
    async fetchConfig() {
      this.startLoading()
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./content/config.json').then(
        (response) => {
          this.stopLoading()
          this._config = response.data as Config
          document.documentElement.setAttribute('dir', this._config.textDirection)
        },
        (error) => {
          this.stopLoading()
          this._config = null
          this.errorMessage = 'Failed to load config.json data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchLocalesIntro() {
      this.startLoading()
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./content/locales/intro.json').then(
        (response) => {
          this.stopLoading()
          this._localesIntro = response.data as LocalesIntro
          this._localesIntroMiscText = response.data['misc-text'] as LocalesIntroMiscText
        },
        (error) => {
          this.stopLoading()
          this._localesIntro = null
          this.errorMessage = 'Failed to load locales intro.json data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchLocalesMotivation() {
      this.startLoading()
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./content/locales/motivation.json').then(
        (response) => {
          this.stopLoading()
          this._localesMotivation = response.data as LocalesMotivation
        },
        (error) => {
          this.stopLoading()
          this._localesMotivation = null
          this.errorMessage = 'Failed to load locales motivation.json data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchLocalesTranslations() {
      this.startLoading()
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./content/locales/translations.json').then(
        (response) => {
          this.stopLoading()
          this._localesTranslations = response.data as LocalesTranslations
        },
        (error) => {
          this.stopLoading()
          this._localesTranslations = null
          this.errorMessage = 'Failed to load locales translations.json data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchCurriculums() {
      this.startLoading()
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./content/curriculum/index.json').then(
        (response) => {
          this.stopLoading()
          this.curriculums = response.data as Curriculums
        },
        (error) => {
          this.stopLoading()
          this._localesIntro = null
          this.errorMessage = 'Failed to load curriculum/index.json data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchChallenge(superblock: string, course: string, slug: string) {
      this.startLoading()
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get(`./content/curriculum/${superblock}/${course}/${slug}.md`).then(
        (response) => {
          this.stopLoading()
          this.challenge = parseChallenge(response.data as string)
          this.resetSolution()
          void this.runTest()
          mathjaxService.removeMathJax()
          mathjaxService.addMathJax()
        },
        (error) => {
          this.stopLoading()
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
    },
    tIntro(key: string): string | string[] {
      if (!this._localesIntro) return ''
      const parts = key.split('.')
      const sbData = this._localesIntro[parts[0]]
      if (!sbData) return ''
      if (parts.length === 2) return sbData[parts[1] as 'title' | 'intro'] ?? ''
      if (parts.length === 4 && parts[1] === 'blocks')
        return sbData.blocks?.[parts[2]]?.[parts[3] as 'title' | 'intro'] ?? ''
      return ''
    },
    getRandomQuote(): { quote: string; author: string } | undefined {
      return this._localesMotivation?.motivationalQuotes.random()
    },
    t(key: string, vars?: Record<string, string>): string {
      const [file, section, name] = key.split('.')
      let value: string | undefined

      if (file === 'translations') {
        value = (this._localesTranslations as Record<string, Record<string, string>> | null)?.[
          section
        ]?.[name]
      } else if (file === 'intro' && section === 'misc-text') {
        value = (this._localesIntroMiscText as Record<string, string> | null)?.[name]
      } else if (file === 'motivation' && section === 'compliment') {
        value = this._localesMotivation?.compliments.random()
      }

      if (!value) return ''
      return vars ? interpolate(value, vars) : value
    }
  }
})

// re-export via function to avoid TS7056 (composite declaration emit limit)
export function useMainStore() {
  return _useMainStore()
}
