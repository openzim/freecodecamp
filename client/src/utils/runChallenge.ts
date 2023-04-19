import { Challenge } from './parseChallenge'
import { assert as chaiAssert } from 'chai'
import * as helpers from './helpers'

// eslint-disable-next-line @typescript-eslint/no-unused-vars
class ChallengeError extends Error {
  assertionError = ''
  constructor(message: string, assertionError: string) {
    super(message)
    this.assertionError = assertionError
  }
}

const escapeQuotes = (str: string) => {
  // return str.replaceAll('"', '\\"')
  return str.replace(/\\([\s\S])|(")/g, '\\$1$2')
}

const setup = ``

const generateEvalCode = (
  solution: string,
  beforeCode: string,
  afterCode: string,
  hints: [string, string][]
): string => {
  const code =
    `
${setup};
${beforeCode};
${solution};
${afterCode};
    ` +
    hints
      .map((hint) => {
        return `
try {
    ${hint[1]};
} catch (e) {
    throw new ChallengeError("${escapeQuotes(hint[0])}", e)
}
`
      })
      .join(';')
  return code
}

export const runChallenge = (challenge: Challenge, code: string) => {
  const evalCode = generateEvalCode(
    code,
    challenge.seedPrecursor || '',
    challenge.seedAddendum || '',
    challenge.hints
  )
  /* eslint-disable @typescript-eslint/no-unused-vars */
  const assert = chaiAssert
  const __helpers = helpers
  /* eslint-enable @typescript-eslint/no-unused-vars */
  // console.log(evalCode)
  // Eval has access to same scope, maybe pull assert out
  eval(evalCode)
}
