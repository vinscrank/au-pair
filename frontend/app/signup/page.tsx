'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { flushSync } from 'react-dom';
import { Wordmark } from '@/components/BrandMark';
import { ApiError, api } from '@/lib/api';
import { useAuth } from '@/lib/auth';
import type { Me } from '@/lib/types';

export default function SignupPage() {
  const router = useRouter();
  const { adopt } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<'candidate' | 'family' | ''>('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (!role) {
      setError('Choose whether you mind children or you need care.');
      return;
    }
    if (password.length < 8) {
      setError('Use at least 8 characters.');
      return;
    }
    setBusy(true);
    setError('');
    try {
      const me = await api<Me>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, role }),
      });
      flushSync(() => adopt(me));
      router.push('/onboarding');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create the account.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="split">
      <section className="split-story">
        <Wordmark />
        <h1 className="display">Two sides, one list.</h1>
        <p className="lede">You will not see anyone until your own profile is filled in. That keeps the pile small.</p>
      </section>
      <section className="split-panel">
        <form className="panel-card stack" onSubmit={submit}>
          <h2 className="display">Create an account</h2>
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
              autoComplete="new-password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              minLength={8}
              required
            />
            <small>At least 8 characters.</small>
          </label>
          <div className="role-grid">
            <button type="button" className={role === 'candidate' ? 'role on' : 'role'} aria-pressed={role === 'candidate'} onClick={() => setRole('candidate')}>
              <span className="eyebrow">Candidate</span>
              <strong>I mind children</strong>
              <span>Au pair or babysitter, any gender.</span>
            </button>
            <button type="button" className={role === 'family' ? 'role on' : 'role'} aria-pressed={role === 'family'} onClick={() => setRole('family')}>
              <span className="eyebrow">Family</span>
              <strong>We need care</strong>
              <span>A host family in Ireland, Dublin first.</span>
            </button>
          </div>
          <button className="btn btn-clay" type="submit" disabled={busy}>
            {busy ? 'Creating account' : 'Continue to your profile'}
          </button>
          <p className="quiet">
            Already registered? <Link href="/login">Sign in</Link>
          </p>
        </form>
      </section>
    </main>
  );
}
