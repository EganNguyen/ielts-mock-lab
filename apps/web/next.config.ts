import type { NextConfig } from 'next'

const staticMode = process.env.NEXT_PUBLIC_STATIC_MODE === '1'
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || ''

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // The dev badge sits on top of the exam's bottom navigation bar.
  devIndicators: false,
  output: staticMode ? 'export' : undefined,
  trailingSlash: staticMode,
  basePath: staticMode ? basePath : undefined,
  assetPrefix: staticMode && basePath ? basePath : undefined,
  images: { unoptimized: true },
  distDir: staticMode ? '.next-static' : '.next',
  ...(staticMode ? {} : {
    async rewrites() {
      const api = process.env.API_PROXY_TARGET || 'http://127.0.0.1:8080'
      return [
        { source: '/api/:path*', destination: `${api}/api/:path*` },
        { source: '/media/:path*', destination: `${api}/media/:path*` },
      ]
    },
  }),
  eslint: { ignoreDuringBuilds: true },
}
export default nextConfig
