/**
 * Meta information about a given challenge
 *
 * @param title - Title of the challenge
 * @param slug - Slug of the challenge
 */
export type ChallengeInfo = { title: string; slug: string }

/**
 * Meta information about a given curriculum, as presented inside index.json file built
 * by the scraper (at curriculum/index.json). Contains a dictionnary, each key is the
 * course slug. The value is a list of challenge information (slug and title).
 */
export type CurriculumInfo = {
  [dict_key: string]: ChallengeInfo[]
}

/**
 * Meta information about all curriculum present in current ZIM, as presented inside
 * index.json file built by the scraper (at curriculum/index.json). Contains a
 * dictionnary, each key is the course slug. The value is a list of challenge
 * information (slug and title)
 */
export type Curriculums = {
  [dict_key: string]: CurriculumInfo
}
