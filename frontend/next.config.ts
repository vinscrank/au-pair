import type { NextConfig } from 'next';

const target = process.env.API_PROXY_TARGET || 'http://127.0.0.1:8000';

const nextConfig: NextConfig = {
  async rewrites() {
    return [{ source: '/uploads/:path*', destination: `${target}/uploads/:path*` }];
  },
};

export default nextConfig;
