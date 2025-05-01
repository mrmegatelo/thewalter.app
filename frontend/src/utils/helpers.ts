import type { FeedType, GenericFeedType, IdentifiableFeedType } from '@/utils/types.ts'

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
    return ''
  }

  const lastPart = parts.pop()

  if (!lastPart) {
    return ''
  }

  return lastPart.split(';').shift() as string
}

type ParamsKey = keyof unknown;
type ParamsValue = string | Array<string>

export function buildUrlWithParams<K extends ParamsKey, V extends ParamsValue>(baseURL: string, params: Record<K, V> = {}): string {
  const url = new URL(baseURL, window.location.origin)

  for (const [key, value] of Object.entries<V>(params)) {
    if (Array.isArray(value)) {
      value.forEach((value) => {
        url.searchParams.append(key, value)
      })
    } else {
      url.searchParams.append(key, value)
    }
  }

  return url.href
}

export function getFeedBaseUrl(type: GenericFeedType): string;
export function getFeedBaseUrl(type: FeedType, id?: string): string;
export function getFeedBaseUrl(type: FeedType, id?: string): string {
  switch (type) {
    // case 'subscription':
    //   return `/api/v1/feed/?subscription_id=${id}`
    // case 'collection':
    //   return `/api/v1/feed/?collection_id=${id}`
    case 'favorites':
      return '/api/v1/feed/?type=favorite'
    case 'articles':
      return '/api/v1/feed/?type=article'
    case 'podcasts':
      return '/api/v1/feed/?type=podcast'
    case 'videos':
      return '/api/v1/feed/?type=video'
    default:
      return '/api/v1/feed/'
  }
}
