import { readFile } from 'fs/promises'
import { join } from 'path'
import { beforeAll, describe, expect, it } from 'vitest'
import { Challenge, parseChallenge, extractKeyValueFromMarkdown } from '../parseChallenge'

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
  it('should pull the header from the markdown', async () => {
    const headers = challenge.header
    expect(typeof headers === 'object').toBe(true)
    expect(headers["title"]).toEqual('Accessing: Object Properties with Variables')
    expect(headers["challengeType"]).toEqual('1')
    expect(headers["dashedName"]).toEqual('accessing-object-properties-with-variables')
    expect(headers["id"]).toEqual('56533eb9ac21ba0edf2244c9')
    expect(headers["videoUrl"]).toEqual('https://scrimba.com/c/cnQyKur')
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

describe('Extract key/value for markdown header', () => {
  it('should parse property with quotes', async () => {
    expect(extractKeyValueFromMarkdown("title: 'A title: with a colon and quotes'")).toEqual(['title', 'A title: with a colon and quotes'])
  })
  it('should parse property without quotes', async () => {
    expect(extractKeyValueFromMarkdown("title: A simple title")).toEqual(['title', 'A simple title'])
  })
  it('should not care about extra spaces', async () => {
    expect(extractKeyValueFromMarkdown("title:   A simple title  ")).toEqual(['title', 'A simple title'])
  })
  it('should not care about extra spaces with quotes', async () => {
    expect(extractKeyValueFromMarkdown("title:  ' A simple title  '   ")).toEqual(['title', ' A simple title  ']) // keep whitespaces inside the quotes
  })
})
