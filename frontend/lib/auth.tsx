'use client';

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { api } from '@/lib/api';
import type { Me } from '@/lib/types';

type AuthValue = {
  user: Me | null;
  loading: boolean;
  refresh: () => Promise<Me | null>;
  logout: () => Promise<void>;
  adopt: (user: Me | null) => void;
};

const AuthContext = createContext<AuthValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<Me | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const me = await api<Me>('/auth/me');
      setUser(me);
      return me;
    } catch {
      setUser(null);
      return null;
    }
  }, []);

  useEffect(() => {
    refresh().finally(() => setLoading(false));
  }, [refresh]);

  const logout = useCallback(async () => {
    try {
      await api('/auth/logout', { method: 'POST' });
    } catch {
      setUser(null);
      return;
    }
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, loading, refresh, logout, adopt: setUser }),
    [user, loading, refresh, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error('AuthProvider missing');
  return value;
}
