export interface BlockInfo {
  title: string
  intro: string[]
}

export interface Blocks {
  [dict_key: string]: BlockInfo
}

export interface LocaleInfo {
  title: string
  intro: string[]
  note: string
  blocks: Blocks
}

export interface Locales {
  [dict_key: string]: LocaleInfo
}
