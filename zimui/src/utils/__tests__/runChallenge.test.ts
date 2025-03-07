import { readFile } from 'fs/promises'
import { join } from 'path'
import { beforeAll, describe, expect, it } from 'vitest'
import { glob } from 'glob'
import { Challenge, parseChallenge } from '../parseChallenge'
import { runChallenge } from '../runChallenge'

describe('Running a basic JS challenge', () => {
  let markdown = ''
  let challenge: Challenge
  beforeAll(async () => {
    markdown = await readFile(join(__dirname, 'fixtures', 'sampleJSChallenge.md'), 'utf-8')
    challenge = parseChallenge(markdown)
  })

  it('should take in a challenge and run a working solution against it', () => {
    const result = runChallenge(challenge, challenge.solutions[0], {
      supressConsole: true
    })
    expect(result.hints.filter((h) => h.passed).length).toEqual(challenge.hints.length)
  })

  it('should log all the console statements for outputting to the user', () => {
    const result = runChallenge(challenge, challenge.solutions[0], {
      supressConsole: true
    })
    expect(result.logs.length).toEqual(1)
    expect(result.logs[0]).toEqual('I should show up on the console')
    expect(result.hints.filter((h) => h.passed).length).toEqual(challenge.hints.length)
  })

  it('should not pass all tests with a bad solution', () => {
    const badSolution = challenge.solutions[1]
    const result = runChallenge(challenge, badSolution)
    expect(result.hints[1].passed).toBe(false)
    expect(result.hints[1].description).toEqual(
      'The variable <code>player</code> should be a string'
    )
  })

  it('should still pass `code` regex tests even when the code throws an exception', () => {
    const badSolution = challenge.solutions[2] // Reference error code
    const result = runChallenge(challenge, badSolution)
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

  it('should throw an error on syntax errors', () => {
    const result = runChallenge(challenge, challenge.solutions[3])
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
      const result = runChallenge(challenge, challenge.solutions[0], {
        supressConsole: true
      })
      expect(result.hints.filter((h) => h.passed).length).toEqual(challenge.hints.length)
    }
  )
})
