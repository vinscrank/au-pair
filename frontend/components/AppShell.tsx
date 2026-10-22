'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Wordmark } from '@/components/BrandMark';
import { useAuth } from '@/lib/auth';

function IconDiscover() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <rect x="4" y="3" width="16" height="18" rx="3" fill="none" stroke="currentColor" strokeWidth="1.8" />
      <path d="M8 8h8M8 12h5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}

function IconMatches() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M5 16.5 12 6l7 10.5" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
      <path d="M8 16h8" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}

function IconProfile() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="9" r="3.2" fill="none" stroke="currentColor" strokeWidth="1.8" />
      <path d="M6 18.5c1.4-2.4 3.4-3.5 6-3.5s4.6 1.1 6 3.5" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}

const LINKS = [
  { href: '/discover', label: 'Discover', icon: IconDiscover },
  { href: '/matches', label: 'Matches', icon: IconMatches },
  { href: '/profile', label: 'Profile', icon: IconProfile },
];

export function AppShell({ children, variant = 'app' }: { children: React.ReactNode; variant?: 'app' | 'plain' }) {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const home = user?.profile_complete ? '/discover' : '/onboarding';

  return (
    <div className={variant === 'app' ? 'shell app' : 'shell'}>
      <header className="topbar">
        <Link href={home} aria-label="Mobijob home">
          <Wordmark compact />
        </Link>
        {variant === 'plain' ? (
          <button type="button" className="text-btn" onClick={() => void logout()}>
            Sign out
          </button>
        ) : null}
      </header>
      <div className="shell-body">{children}</div>
      {variant === 'app' ? (
        <nav className="nav">
          {LINKS.map((link) => {
            const Icon = link.icon;
            const on = pathname === link.href;
            return (
              <Link key={link.href} href={link.href} className={on ? 'on' : undefined} aria-current={on ? 'page' : undefined}>
                <Icon />
                {link.label}
              </Link>
            );
          })}
        </nav>
      ) : null}
    </div>
  );
}
