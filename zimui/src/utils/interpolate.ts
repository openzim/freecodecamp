export function interpolate(str: string, vars: Record<string, string>): string {
  return str.replace(/\{\{\s*(\w+)\s*\}\}/g, (_, key) => {
    if (!(key in vars)) {
      console.warn(`Missing a placeholder value for "{{${key}}}"`)
    }
    return vars[key] || ''
  })
}
