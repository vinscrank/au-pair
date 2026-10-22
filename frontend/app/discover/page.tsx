'use client';

import { useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AppShell } from '@/components/AppShell';
import { SwipeDeck } from '@/components/SwipeDeck';
import { ApiError, api } from '@/lib/api';
import { useAuth } from '@/lib/auth';
import type { Card, SwipeResponse } from '@/lib/types';

export default function DiscoverPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [cards, setCards] = useState<Card[] | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    api<{ cards: Card[] }>('/discover')
      .then((data) => {
        if (active) setCards(data.cards);
      })
      .catch((err) => {
        if (err instanceof ApiError && err.status === 403) {
          router.replace('/onboarding');
          return;
        }
        if (active) setError(err instanceof ApiError ? err.message : 'Could not load profiles.');
      });
    return () => {
      active = false;
    };
  }, [router]);

  const onSwipe = useCallback((card: Card, direction: 'like' | 'pass') => {
    return api<SwipeResponse>('/swipes', {
      method: 'POST',
      body: JSON.stringify({ target_id: card.user_id, direction }),
    });
  }, []);

  const interest = user?.role === 'family' ? 'Send interest' : 'Apply';

  return (
    <AppShell>
      <div className="discover-layout">
        <aside className="discover-aside">
          <div>
            <p className="eyebrow">Dublin</p>
            <h1 className="display">Care, without the group chat.</h1>
            <p>Pass, or show interest. WhatsApp opens only when it is mutual.</p>
          </div>
          <p className="quiet">Arrow keys work here too. Left to pass, right to {interest.toLowerCase()}.</p>
        </aside>
        <div className="deck-wrap">
          {error ? (
            <p className="alert" role="alert">
              {error}
            </p>
          ) : null}
          {cards === null && !error ? <p>Loading profiles</p> : null}
          {cards ? <SwipeDeck cards={cards} interestLabel={interest} onSwipe={onSwipe} /> : null}
        </div>
      </div>
    </AppShell>
  );
}
