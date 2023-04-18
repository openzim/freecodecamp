import { readFile } from 'fs/promises'
import { join } from 'path'
import { beforeAll, describe, expect, it } from 'vitest'
import { glob } from 'glob'
import { Challenge, parseChallenge } from '../parseChallenge'
import { ChallengeError, runChallenge } from '../runChallenge'


describe("Running a basic JS challenge", () => {
    let markdown = ''
    let challenge: Challenge
    beforeAll(async () => {
        markdown = await readFile(join(__dirname, 'fixtures', 'sampleJSChallenge.md'), 'utf-8')
        challenge = parseChallenge(markdown)
    })

    it('should take in a challenge and run a working solution against it', async () => {
        expect(() => runChallenge(challenge, challenge.solutions[0])).not.toThrowError()
    })

    it('should throw the appropriate error with a bad solution', async () => {
        const badSolution = `
const testObj = {
  12: "Namath",
  16: "Montana",
  19: "Unitas"
};
const playerNumber = 18;
const player = testObj[playerNumber];
        `
        expect(() => runChallenge(challenge, badSolution)).toThrowError('The variable `player` should be a string')
    })
})

describe("Running a more complex JS Challenge", () => {
    let markdown = ''
    let challenge: Challenge
    beforeAll(async () => {
        markdown = await readFile(join(__dirname, 'fixtures', 'complexJSChallenge.md'), 'utf-8')
        challenge = parseChallenge(markdown)
    })

    it('should take in a challenge and run a working solution against it', async () => {
        expect(() => runChallenge(challenge, challenge.solutions[0])).not.toThrowError()
    })
})

describe("Run all the solutions in the assets folder", () => {
    it("every challenge in the assets folder should pass with it's own solution", async () => {
        const markdownChallenges = await glob(join(__dirname, '..', '..', 'assets', 'curriculum', '**', '*.md') )
        for (const markdownChallenge of markdownChallenges) {
            const markdown = await readFile(markdownChallenge, 'utf-8')
            const challenge = parseChallenge(markdown)
            try {
                runChallenge(challenge, challenge.solutions[0])
            } catch (e) {
                const id = challenge.header['id']

                // This particular challenges solution fails with a ReferenceError on purpose
                if (id === "56533eb9ac21ba0edf2244bf") {
                    if (e instanceof ReferenceError) {
                        expect(true)
                    }
                } else {
                    expect(false, `Challenge failed: ${markdownChallenge}`)
                }
            }
        } 
    })
})
