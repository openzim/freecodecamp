import { marked } from 'marked'

export const parseChallenge = (markdownStr: string): Challenge => {
  return new Challenge(marked.lexer(markdownStr))
}

type HintTokens =
  | marked.Tokens.Space
  | marked.Tokens.Code
  | marked.Tokens.Paragraph

export class Challenge {
  tokensList: marked.TokensList

  constructor(tokensList: marked.TokensList) {
    this.tokensList = tokensList
  }

  get header() {
    if (this.tokensList[1] && this.tokensList[1].type === 'heading') {
      const frontMatter = this.tokensList[1] as marked.Tokens.Heading
      const rawStrings = frontMatter.text.split('\n')
      const data: { [key: string]: string } = {}
      for (const rawString of rawStrings) {
        const keyVal = rawString.split(': ')
        data[keyVal[0]] = keyVal[1]
      }
      return data
    }
    throw new Error('Unable to parse heading data')
  }

  get hints(): [hint: string, assertion: string][] {
    const solutionsToken = this.getSectionTokens('--hints--')
    const assertions: [string, string][] = []
    let currentHint: string | null = null
    if (solutionsToken) {
      for (const solutionToken of solutionsToken as HintTokens[]) {
        if (solutionToken.type === 'paragraph') {
          currentHint = solutionToken.text
        } else if (solutionToken.type === 'code' && currentHint) {
          assertions.push([currentHint, solutionToken.text])
          currentHint = null
        }
      }
    }
    return assertions
  }

  get seed(): string | null {
    return this.getSectionCodes('--seed-contents--')[0] || null
  }

  get seedPrecursor(): string | null {
    return this.getSectionCodes('--before-user-code--')[0] || null
  }

  get seedAddendum(): string | null {
    return this.getSectionCodes('--after-user-code--')[0] || null
  }

  get solutions(): string[] {
    return this.getSectionCodes('solutions')
  }

  get description(): string {
    const descriptionMarkdown = this.getSectionMarkdown('description')
    if (!descriptionMarkdown) {
      throw new Error('No description in challenge')
    }
    return descriptionMarkdown
  }

  get instructions(): string {
    const instructionMarkdown = this.getSectionMarkdown('instructions')
    if (!instructionMarkdown) {
      throw new Error('No description in challenge')
    }
    return instructionMarkdown
  }

  toJSON() {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const json: any = this.header
    json.solutions = this.solutions
    json.description = this.description
    return json
  }

  private getSectionTokens(title: string): marked.Token[] | null {
    const tokens: marked.Token[] = []
    let inHeading = false
    for (const token of this.tokensList) {
      if (token.type === 'heading' && token.raw.match(title)) {
        inHeading = true
      } else if (token.type === 'heading') {
        inHeading = false
      } else if (inHeading) {
        tokens.push(token)
      }
    }
    return tokens
  }

  private getSectionMarkdown(title: string): string | null {
    const sectionTokens = this.getSectionTokens(title)
    if (sectionTokens) {
      const markdown = sectionTokens?.map((token) => token.raw).join('')
      return markdown
    }
    return null
  }

  private getSectionCodes(title: string): string[] {
    const sectionTokens = this.getSectionTokens(title)
    const codes = []
    if (sectionTokens) {
      for (const solutionToken of sectionTokens as marked.Tokens.Code[]) {
        if (solutionToken.type === 'code') {
          codes.push(solutionToken.text)
        }
      }
    }
    return codes
  }
}
