import type { NextRequest } from 'next/server';

export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

const HOP = new Set(['host', 'connection', 'content-length', 'accept-encoding']);

async function proxy(request: NextRequest, context: { params: Promise<{ path: string[] }> }) {
  const { path } = await context.params;
  const target = process.env.API_PROXY_TARGET || 'http://127.0.0.1:8000';
  const url = `${target}/api/${path.join('/')}${request.nextUrl.search}`;
  const headers = new Headers();
  request.headers.forEach((value, key) => {
    if (!HOP.has(key.toLowerCase())) headers.set(key, value);
  });
  const hasBody = request.method !== 'GET' && request.method !== 'HEAD';
  const response = await fetch(url, {
    method: request.method,
    headers,
    body: hasBody ? Buffer.from(await request.arrayBuffer()) : undefined,
    cache: 'no-store',
    redirect: 'manual',
  });
  const out = new Headers();
  const type = response.headers.get('content-type');
  if (type && response.status !== 204 && response.status !== 205) out.set('content-type', type);
  for (const cookie of response.headers.getSetCookie()) {
    out.append('set-cookie', cookie);
  }
  if (response.status === 204 || response.status === 205 || response.status === 304) {
    return new Response(null, { status: response.status, headers: out });
  }
  return new Response(await response.arrayBuffer(), { status: response.status, headers: out });
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
