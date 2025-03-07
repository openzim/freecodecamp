/**
 * Information about a given course / block
 *
 * @param title - Title of the course
 * @param intro -  Introduction of the block (list of paragraphs)
 */
export interface BlockInfo {
  title: string
  intro: string[]
}

/**
 * Generic information about FCC courses, presented as a dict of block / course slug to
 * course / block information. File format comes from FCC file at  locales/intro.json
 */
export interface Blocks {
  [dict_key: string]: BlockInfo
}

/**
 * Information about a given superblock/curriculum in FCC format
 *
 * @param title - Title of the superblock
 * @param intro - Introduction of the superblock (list of paragraphs)
 * @param note - Note on the superblock
 * @param blocks - Information on the blocks (i.e. courses)
 */
export interface LocaleIntroInfo {
  title: string
  intro: string[]
  note: string
  blocks: Blocks
}

/**
 * Generic information about FCC superblock and blocks, presented as a dict of
 * superblock slug to superblock information. File format comes from FCC file at
 * locales/intro.json (for proper language).
 */
export interface LocalesIntro {
  [dict_key: string]: LocaleIntroInfo
}

/**
 * Miscelaneous text for UI
 */
export interface LocalesIntroMiscText {
  courses: string
  expand: string
  collapse: string
}

/**
 * Motivational strings. File comes from FCC file at locales/motivation.json.
 */
export interface LocalesMotivation {
  compliments: string[]
  motivationalQuotes: {
    quote: string
    author: string
  }[]
}

/**
 * Translations strings. File comes from FCC file at locales/translations.json.
 */
export interface LocalesTranslations {
  learn: {
    [dict_key: string]: string
  }
  buttons: {
    [dict_key: string]: string
  }
}
