import { readFile } from 'fs/promises'
import { join } from 'path'
import { beforeAll, describe, expect, it } from 'vitest'
import { Challenge, parseChallenge } from '../parseChallenge'

describe('Parsing a basic JS challenge', () => {
  let markdown = ''
  let challenge: Challenge
  beforeAll(async () => {
    markdown = await readFile(
      join(__dirname, 'fixtures', 'basicMarkdownChallenge.md'),
      'utf-8'
    )
    challenge = parseChallenge(markdown)
  })
  it('should take in FCC markdown as parse description from it', async () => {
    const description = challenge.description
    expect(typeof description === 'string').toBe(true)
    expect(description && description.length > 0).toBe(true)
  })
  it('should pull the seed code from the markdown', async () => {
    const seed = challenge.seed
    expect(typeof seed === 'string').toBe(true)
  })
  it('should parse the hints from the markdown', async () => {
    const hints = challenge.hints
    expect(hints.length).toEqual(6)
  })
  it('should get the solution from the markdown', async () => {
    const solutions = challenge.solutions
    expect(solutions.length).toEqual(1)
    expect(typeof solutions[0] === 'string').toBe(true)
  })
})
