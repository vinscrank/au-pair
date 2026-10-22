'use client';

import { usePathname, useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { Wordmark } from '@/components/BrandMark';
import { useAuth } from '@/lib/auth';
import type { Me } from '@/lib/types';

function destination(user: Me | null, pathname: string): string | null {
  const isPublic = pathname === '/' || pathname === '/login' || pathname === '/signup';
  if (!user && !isPublic) return '/login';
  if (user && (pathname === '/login' || pathname === '/signup' || pathname === '/')) {
    return user.profile_complete ? '/discover' : '/onboarding';
  }
  if (user && !user.profile_complete && (pathname === '/discover' || pathname === '/matches' || pathname === '/profile')) {
    return '/onboarding';
  }
  return null;
}

export function Guard({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  const next = loading ? null : destination(user, pathname);

  useEffect(() => {
    if (next && next !== pathname) router.replace(next);
  }, [next, pathname, router]);

  if (loading || (next && next !== pathname)) {
    return (
      <div className="boot">
        <Wordmark />
      </div>
    );
  }

  return children;
}
