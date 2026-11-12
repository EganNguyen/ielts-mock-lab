import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // The dev badge sits on top of the exam's bottom navigation bar.
  devIndicators: false,
  async rewrites() {
    const api = process.env.API_PROXY_TARGET || 'http://127.0.0.1:8080'
    return [
      { source: '/api/:path*', destination: `${api}/api/:path*` },
      { source: '/media/:path*', destination: `${api}/media/:path*` },
    ]
  },
  eslint: { ignoreDuringBuilds: true },
}
export default nextConfig
