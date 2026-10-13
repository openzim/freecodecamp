import { readFileSync } from 'fs'
import { readFile } from 'fs/promises'
import { join } from 'path'
import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest'
import { glob } from 'glob'
import { Challenge, parseChallenge } from '../parseChallenge'
import { runChallenge } from '../runChallenge'

// jsdom has no Worker implementation, so runChallenge.ts's JSTestWorker can't
// spin up a real one here. This fakes just enough of the Worker/postMessage
// contract to run the *real* @freecodecamp/curriculum-helpers
// javascript-test-evaluator.js (same chai + helpers bundle used in
// production) synchronously in this process, by `eval`-ing it the same way a
// browser would run it as a worker's global script (it defines a bare global
// `onmessage` and only ever replies via the MessagePort it's given, see
// https://github.com/freeCodeCamp/curriculum-helpers packages/javascript-evaluator).
const evaluatorScript = readFileSync(
  join(
    __dirname,
    '..',
    '..',
    '..',
    'node_modules',
    '@freecodecamp',
    'curriculum-helpers',
    'dist',
    'test-runner',
    'javascript-test-evaluator.js'
  ),
  'utf-8'
)

type MessageHandler = ((e: { data: unknown; ports: MessagePort[] }) => void) | null

class FakeWorker {
  #onmessage: MessageHandler = null

  constructor() {
    const scope = globalThis as unknown as {
      onmessage: MessageHandler
      importScripts?: () => void
    }
    // The bundled webpack runtime auto-detects its publicPath from
    // `self.importScripts` being defined (true in a real Worker scope) before
    // ever falling back to looking for a <script> tag (which jsdom has none
    // of here, since this isn't really running as one); stub it so it takes
    // that first branch instead of throwing.
    scope.importScripts ??= () => {}

    ;(0, eval)(evaluatorScript)
    this.#onmessage = scope.onmessage
    scope.onmessage = null
  }

  postMessage(data: unknown, options?: { transfer?: MessagePort[] }) {
    this.#onmessage?.({ data, ports: options?.transfer ?? [] })
  }

  terminate() {
    // no-op: nothing to clean up outside of the shared eval scope
  }
}

beforeAll(() => {
  vi.stubGlobal('Worker', FakeWorker)
})

afterAll(() => {
  vi.unstubAllGlobals()
})

describe('Running a basic JS challenge', () => {
  let markdown = ''
  let challenge: Challenge

  beforeAll(async () => {
    markdown = await readFile(join(__dirname, 'fixtures', 'sampleJSChallenge.md'), 'utf-8')
    challenge = parseChallenge(markdown)
  })

  it('should take in a challenge and run a working solution against it', async () => {
    const result = await runChallenge(challenge, challenge.solutions[0], {
      supressConsole: true
    })
    expect(result.hints.filter((h) => h.passed).length).toEqual(challenge.hints.length)
  })

  it('should log all the console statements for outputting to the user', async () => {
    const result = await runChallenge(challenge, challenge.solutions[0], {
      supressConsole: true
    })
    expect(result.logs.length).toEqual(1)
    expect(result.logs[0]).toEqual('I should show up on the console')
    expect(result.hints.filter((h) => h.passed).length).toEqual(challenge.hints.length)
  })

  it('should not pass all tests with a bad solution', async () => {
    const badSolution = challenge.solutions[1]
    const result = await runChallenge(challenge, badSolution, { supressConsole: true })
    expect(result.hints[1].passed).toBe(false)
    expect(result.hints[1].description).toEqual(
      'The variable <code>player</code> should be a string'
    )
  })

  it('should still pass `code` regex tests even when the code throws an exception', async () => {
    const badSolution = challenge.solutions[2] // Reference error code
    const result = await runChallenge(challenge, badSolution, { supressConsole: true })
    expect(result.hints[1].passed).toBe(false)
    expect(result.hints[1].description).toEqual(
      'The variable <code>player</code> should be a string'
    )

    // Code matcher still pass
    expect(result.hints[3].passed).toBe(true)
    expect(result.hints[3].description).toEqual(
      'You should use bracket notation to access <code>testObj</code>'
    )

    // Log the error
    expect(result.logs[0]).toEqual('ReferenceError: someUnknownVariable is not defined')
  })

  it('should throw an error on syntax errors', async () => {
    const result = await runChallenge(challenge, challenge.solutions[3], {
      supressConsole: true
    })
    expect(result.logs[0]).toEqual('SyntaxError: Unexpected number')
  })
})

describe('Run all the solutions in the dist folder', async () => {
  // In development mode 'dist' doesn't exist, use public as a possible fallback
  let markdownChallenges = await glob(
    join(__dirname, '..', '..', '..', 'dist', 'fcc', 'curriculum', '**', '*.md')
  )
  if (markdownChallenges.length === 0) {
    markdownChallenges = await glob(
      join(__dirname, '..', '..', 'public', 'fcc', 'curriculum', '**', '*.md')
    )
  }
  if (markdownChallenges.length === 0) {
    it.skip('No markdown challenges found in the curriculum to run')
    return
  }

  it.each(markdownChallenges)(
    "every challenge in the assets folder should pass with it's own solution",
    async (markdownChallenge) => {
      const markdown = await readFile(markdownChallenge, 'utf-8')
      const challenge = parseChallenge(markdown)
      const result = await runChallenge(challenge, challenge.solutions[0], {
        supressConsole: true
      })
      expect(result.hints.filter((h) => h.passed).length).toEqual(challenge.hints.length)
    }
  )
})
