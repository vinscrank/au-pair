'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AppShell } from '@/components/AppShell';
import { DetailSheet } from '@/components/DetailSheet';
import { ApiError, api } from '@/lib/api';
import { whatsappHref } from '@/lib/phone';
import type { Match } from '@/lib/types';

export default function MatchesPage() {
  const router = useRouter();
  const [matches, setMatches] = useState<Match[] | null>(null);
  const [open, setOpen] = useState<Match | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api<{ matches: Match[] }>('/matches')
      .then((data) => setMatches(data.matches))
      .catch((err) => {
        if (err instanceof ApiError && err.status === 403) {
          router.replace('/onboarding');
          return;
        }
        setError(err instanceof ApiError ? err.message : 'Could not load matches.');
      });
  }, [router]);

  return (
    <AppShell>
      <div className="page">
        <p className="eyebrow">Matches</p>
        <h1 className="display">People who said yes back.</h1>
        {error ? (
          <p className="alert" role="alert">
            {error}
          </p>
        ) : null}
        {matches && matches.length === 0 ? (
          <div className="empty-card">
            <p>When it is mutual, they show up here, with WhatsApp.</p>
          </div>
        ) : null}
        <div className="stack">
          {matches?.map((match) => {
            const whatsapp = match.contact.available && match.contact.value ? match.contact.value : null;
            return (
              <article key={match.id} className="match-card">
                <button type="button" className="match-open" onClick={() => setOpen(match)}>
                  {match.card.photo_url ? <img src={match.card.photo_url} alt="" /> : <span className="portrait-fallback">{match.card.display_name.slice(0, 1)}</span>}
                  <span>
                    <strong>{match.card.display_name}</strong>
                    <small>{match.card.headline}</small>
                  </span>
                </button>
                {whatsapp ? (
                  <a className="btn btn-clay" href={whatsappHref(whatsapp)} target="_blank" rel="noreferrer">
                    WhatsApp
                  </a>
                ) : (
                  <p className="quiet">WhatsApp is not open on this match yet.</p>
                )}
              </article>
            );
          })}
        </div>
      </div>
      {open ? <DetailSheet card={open.card} contact={open.contact} onClose={() => setOpen(null)} /> : null}
    </AppShell>
  );
}
