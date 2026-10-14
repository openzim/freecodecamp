import { createPinia, setActivePinia } from 'pinia'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useMainStore } from '@/stores/main'

const { mockedGet } = vi.hoisted(() => ({ mockedGet: vi.fn() }))
vi.mock('axios', () => ({
  default: { get: mockedGet, isAxiosError: vi.fn() },
  AxiosError: class AxiosError extends Error {}
}))

describe('main store isLoading', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('defaults to loading before any fetch is issued', () => {
    const main = useMainStore()
    expect(main.isLoading).toBe(true)
  })

  it('stays true until every concurrent fetch has settled, like HeaderBar.vue does on mount', async () => {
    const main = useMainStore()

    // One resolver per endpoint, so each request can be settled independently and
    // out of order, the way real concurrent network requests would complete.
    const resolvers: Array<() => void> = []
    mockedGet.mockImplementation(() => {
      return new Promise((resolve) => {
        resolvers.push(() => resolve({ data: {} }))
      })
    })

    const all = Promise.all([
      main.fetchConfig(),
      main.fetchLocalesIntro(),
      main.fetchCurriculums(),
      main.fetchLocalesMotivation(),
      main.fetchLocalesTranslations()
    ])

    expect(resolvers).toHaveLength(5)
    expect(main.isLoading).toBe(true)

    // Settle them one at a time, in a different order than they were issued:
    // isLoading must stay true as long as any request is still pending.
    for (const resolver of [resolvers[2], resolvers[0], resolvers[3], resolvers[4]]) {
      resolver()
      await Promise.resolve()
      expect(main.isLoading).toBe(true)
    }

    resolvers[1]()
    await all

    expect(main.isLoading).toBe(false)
  })
})
