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
export interface LocaleInfo {
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
export interface Locales {
  [dict_key: string]: LocaleInfo
}
