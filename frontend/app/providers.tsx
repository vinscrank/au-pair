'use client';

import { AuthProvider } from '@/lib/auth';
import { Guard } from '@/components/Guard';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <Guard>{children}</Guard>
    </AuthProvider>
  );
}
