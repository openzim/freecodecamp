//  declare window.MathJax so that we can manipulate it without TS errors
declare global {
  interface Window {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    MathJax: any
  }
}

export {}
