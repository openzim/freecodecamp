/**
 * Meta information about a given challenge
 *
 * @param title - Title of the challenge
 * @param slug - Slug of the challenge
 */
export type ChallengeInfo = { title: string; slug: string }

/**
 * Meta information about challenges of a course, as presented inside _meta.json FCC
 * files for a given course (files at curriculum/${superblock}/${course}/_meta.json)
 *
 * @param challenges - List of challenges information for this course
 */
export type ChallengesMeta = {
  challenges: ChallengeInfo[]
}
