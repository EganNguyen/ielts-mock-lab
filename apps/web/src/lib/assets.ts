export const STATIC_MODE = process.env.NEXT_PUBLIC_STATIC_MODE === '1'
export const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH || ''

/** Prefix a runtime asset path such as /media/... with the GitHub Pages base path. */
export function assetUrl(path?: string | null): string {
  if (!path) return ''
  if (!BASE_PATH || path.startsWith(`${BASE_PATH}/`) || path === BASE_PATH) return path
  return `${BASE_PATH}${path.startsWith('/') ? '' : '/'}${path}`
}
