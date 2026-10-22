'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { flushSync } from 'react-dom';
import { Wordmark } from '@/components/BrandMark';
import { ApiError, api } from '@/lib/api';
import { useAuth } from '@/lib/auth';
import type { Me } from '@/lib/types';

export default function LoginPage() {
  const router = useRouter();
  const { adopt } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError('');
    try {
      const me = await api<Me>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });
      flushSync(() => adopt(me));
      router.push(me.profile_complete ? '/discover' : '/onboarding');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not sign in.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="split">
      <section className="split-story">
        <Wordmark />
        <h1 className="display">Welcome back.</h1>
        <p className="lede">Pick up your Dublin search where you left it.</p>
      </section>
      <section className="split-panel">
        <form className="panel-card stack" onSubmit={submit}>
          <h2 className="display">Sign in</h2>
          {error ? (
            <div className="alert" role="alert">
              {error}
            </div>
          ) : null}
          <label className="field">
            <span>Email</span>
            <input type="email" autoComplete="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
          </label>
          <label className="field">
            <span>Password</span>
            <input
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </label>
          <button className="btn btn-clay" type="submit" disabled={busy}>
            {busy ? 'Signing in' : 'Sign in'}
          </button>
          <p className="quiet">
            New here? <Link href="/signup">Create an account</Link>
          </p>
        </form>
      </section>
    </main>
  );
}
