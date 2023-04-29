/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['i.pravatar.cc'],
  },
  publicRuntimeConfig: {
    baseRestUrl: 'http://localhost:8000/api/limbo',
  }
}

module.exports = nextConfig
