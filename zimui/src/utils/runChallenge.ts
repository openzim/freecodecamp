import { Challenge } from './parseChallenge'

export type RunResultHint = {
  description: string
  passed: boolean
}

export type RunResult = {
  logs: string[]
  hints: RunResultHint[]
}

type TestLog = { level: 'trace' | 'debug' | 'info' | 'log' | 'warn' | 'error'; msg: string }
type TestOutcome =
  { pass: true; logs?: TestLog[] } | { err: { message: string; stack?: string }; logs?: TestLog[] }
type WorkerInitOptions = { source?: string; code?: { contents?: string } }

// Served by vite.config.ts's vite-copy-test-runner-assets plugin, copied from
// @freecodecamp/curriculum-helpers' dist/test-runner. We only use the
// "javascript" evaluator: see src/constants.ts for the challenge types we support.
const TEST_RUNNER_SCRIPT_URL = `${import.meta.env.BASE_URL}test-runner/javascript-test-evaluator.js`

/**
 * Thin host-side half of @freecodecamp/curriculum-helpers' worker test-runner
 * message protocol. We can't import their WorkerTestRunner directly: its
 * published dist/test-runner/index.js is a plain side-effecting script
 * (assigns `window.FCCTestRunner`), not an ES module, so it only works loaded
 * as a <script> tag. The actual test logic (bundled chai + curriculum
 * helpers, eval/hooks semantics) still comes entirely from their
 * javascript-test-evaluator.js worker script; this class only replicates the
 * small postMessage/MessageChannel RPC used to talk to it.
 */
class JSTestWorker {
  #worker: Worker
  #opts: WorkerInitOptions | null = null

  constructor() {
    this.#worker = new Worker(TEST_RUNNER_SCRIPT_URL)
  }

  #post<T>(message: unknown): Promise<T> {
    return new Promise((resolve) => {
      const channel = new MessageChannel()
      channel.port1.onmessage = (event) => {
        channel.port1.close()
        resolve(event.data as T)
      }
      this.#worker.postMessage(message, { transfer: [channel.port2] })
    })
  }

  async init(opts: WorkerInitOptions): Promise<void> {
    this.#opts = opts
    await this.#post({ type: 'init', value: opts })
  }

  async #recreate(): Promise<void> {
    this.#worker = new Worker(TEST_RUNNER_SCRIPT_URL)
    if (this.#opts) {
      await this.#post({ type: 'init', value: this.#opts })
    }
  }

  async runTest(test: string, timeout = 5000): Promise<TestOutcome> {
    let timeoutId!: ReturnType<typeof setTimeout>
    const timedOut = new Promise<TestOutcome>((resolve) => {
      timeoutId = setTimeout(() => {
        this.#worker.terminate()
        void this.#recreate().then(() => resolve({ err: { message: 'Test timed out' } }))
      }, timeout)
    })
    const result = this.#post<{ value: TestOutcome }>({ type: 'test', value: test }).then(
      ({ value }) => value
    )
    try {
      return await Promise.race([result, timedOut])
    } finally {
      clearTimeout(timeoutId)
    }
  }

  dispose(): void {
    this.#worker.terminate()
  }
}

// Reused across challenges: creating a new worker means re-fetching/parsing
// its ~140kB script, so we keep one around and just re-init() it per challenge.
let jsTestWorker: JSTestWorker | null = null

export const runChallenge = async (
  challenge: Challenge,
  code: string,
  options?: { supressConsole: boolean }
): Promise<RunResult> => {
  const result: RunResult = {
    logs: [],
    hints: challenge.hints.map((hint) => ({
      passed: false,
      description: hint[0].replace(/`(.*?)`/g, '<code>$1</code>')
    }))
  }

  const source = [challenge.seedPrecursor, code, challenge.seedAddendum]
    .filter((part): part is string => Boolean(part))
    .join(';\n')

  try {
    jsTestWorker ??= new JSTestWorker()
    await jsTestWorker.init({ source, code: { contents: code } })

    for (let i = 0; i < challenge.hints.length; i++) {
      const [, assertion] = challenge.hints[i]
      const outcome = await jsTestWorker.runTest(assertion)
      result.hints[i].passed = 'pass' in outcome

      // `source` re-runs on every hint, so its console output is identical
      // across calls: only keep the first run's logs to avoid showing the
      // same lines once per hint.
      if (i === 0) {
        for (const log of outcome.logs ?? []) {
          result.logs.push(log.msg)
          if (!options?.supressConsole) {
            console[log.level](log.msg)
          }
        }
      }
    }
  } catch (e: unknown) {
    result.logs.push(e instanceof Error ? e.toString() : JSON.stringify(e))
  }

  return result
}
