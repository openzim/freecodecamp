import { Challenge } from './parseChallenge'
import { assert as chaiAssert } from 'chai'
import * as helpers from './helpers'

// const escapeQuotes = (str: string) => {
//   // return str.replaceAll('"', '\\"')
//   return str.replace(/\\([\s\S])|(")/g, '\\$1$2')
// }

// Hijack console logging statements
const ___setupEvalCode = () => {
  return `
const console = ___consoleProxy;\n
  `
}

// Loop though hints and mark them pass/fail
const ___hintEvalCode = (hints: [string, string][]): string => {
  return hints
    .map((hint, i) => {
      return `
try {
  if (___result.hints[${i}] !== true) {
    ${hint[1]};
    ___result.hints[${i}].passed = true;
  }
} catch (e) {
  ___result.hints[${i}].passed = false;
}
`
    })
    .join('\n')
}

/**
 * Should look something like
 *
 * setupCode
 * try {
 *   beforeCode
 *   userCode
 *   afterCode
 *   try {
 *      hint[i]
 *   } catch (e) {
 *      markHint[i] failed
 *   }
 * } catch (e) {
 *   appendErrors to log
 * }
 * try {
 *    hint[i]
 * } catch (e) {
 *    markHint[i] failed
 * }
 *
 * @param solution
 * @param beforeCode
 * @param afterCode
 * @param hints
 * @returns
 */

const ___generateEvalCode = (
  solution: string,
  beforeCode: string,
  afterCode: string,
  hints: [string, string][]
): string => {
  const code = `
${___setupEvalCode()};
try {
  ${beforeCode};
  ${solution};
  ${afterCode};
  ${___hintEvalCode(hints)}
} catch (e) {
  ___result.logs.push(e.toString());
  ${___hintEvalCode(hints)}
}
`
  return code
}

export type RunResult = {
  logs: string[]
  hints: {
    description: string
    passed: boolean
  }[]
}

export const runChallenge = (
  ___challenge: Challenge,
  code: string,
  ___options?: { supressConsole: boolean }
): RunResult => {
  const ___result: RunResult = {
    logs: [],
    hints: ___challenge.hints.map((hint) => ({
      passed: false,
      description: hint[0],
    })),
  }
  const ___evalCode = ___generateEvalCode(
    code,
    ___challenge.seedPrecursor || '',
    ___challenge.seedAddendum || '',
    ___challenge.hints
  )

  const ___originalConsole = console
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const ___consoleFn = (...msg: any[]) => {
    ___result.logs.push(...msg)
    if (!___options?.supressConsole) {
      // eslint-disable-next-line no-console
      ___originalConsole.log(...msg)
    }
  }

  /* eslint-disable @typescript-eslint/no-unused-vars */
  const ___consoleProxy = {
    log: ___consoleFn,
    debug: ___consoleFn,
    info: ___consoleFn,
    warn: ___consoleFn,
    error: ___consoleFn,
  }
  const assert = chaiAssert
  const __helpers = helpers
  /* eslint-enable @typescript-eslint/no-unused-vars */
  eval(___evalCode)
  return ___result
}
