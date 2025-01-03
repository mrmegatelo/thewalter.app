export function debounce<F extends (...args: Parameters<F>) => unknown>(fn: F, delay: number) {
  let timeoutId: number
  return function(this: unknown, ...args: Parameters<F>) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

export function getCookie(name: string): string {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length !== 2) {
    return ""
  }

  const lastPart = parts.pop()

  if (!lastPart) {
    return ""
  }

  return lastPart.split(';').shift() as string
}
