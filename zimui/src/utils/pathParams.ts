export const singlePathParam = (param: string | string[]): string => {
  if (Array.isArray(param)) {
    if (param.length != 1) {
      throw Error('Improper param length: ' + param)
    }
    return param[0]
  }
  return param
}
