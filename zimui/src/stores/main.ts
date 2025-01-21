import { defineStore } from 'pinia'
import axios, { AxiosError } from 'axios'
import type { Locales } from '../types/locales.ts'
import type { ChallengeInfo, ChallengesMeta } from '../types/challenges.ts'
import { parseChallenge } from '@/utils/parseChallenge.ts'
import type { Challenge } from '@/utils/parseChallenge.ts'
import mathjaxService from '@/services/mathjax'

export type RootState = {
  locales: Locales | null
  challengesMeta: ChallengesMeta | null
  challenge: Challenge | null
  solution: string
  logs: string[]
  isLoading: boolean
  errorMessage: string
  errorDetails: string
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const nextChallenge = function (state: any) {
  return (slug: string): ChallengeInfo | undefined => {
    if (!state.challenge || !state.challengesMeta) {
      return undefined
    }
    const challengeIndex = state.challengesMeta.challenges.findIndex(
      (c: ChallengeInfo) => c.slug === slug
    )
    if (challengeIndex <= state.challengesMeta.challenges.length) {
      return state.challengesMeta.challenges[challengeIndex + 1]
    }
    return undefined
  }
}

export const useMainStore = defineStore('main', {
  state: () =>
    ({
      locales: null,
      challengesMeta: null,
      challenge: null,
      solution: '',
      logs: [],
      isLoading: false,
      errorMessage: '',
      errorDetails: ''
    }) as RootState,
  getters: {
    nextChallenge: nextChallenge
  },
  actions: {
    async fetchLocales() {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get('./content/locales/intro.json').then(
        (response) => {
          this.isLoading = false
          this.locales = response.data as Locales
        },
        (error) => {
          this.isLoading = false
          this.locales = null
          this.errorMessage = 'Failed to load locales data.'
          if (error instanceof AxiosError) {
            this.handleAxiosError(error)
          }
        }
      )
    },
    async fetchMeta(superblock: string, course: string) {
      this.isLoading = true
      this.errorMessage = ''
      this.errorDetails = ''

      return axios.get(`./content/curriculum/${superblock}/${course}/_meta.json`).then(
        (response) => {
          this.isLoading = false
          this.challengesMeta = response.data as ChallengesMeta
        },
        (error) => {
          this.isLoading = false
          this.challengesMeta = null
          this.errorMessage = `Failed to load challenges meta data for ${superblock}/${course}.`
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
