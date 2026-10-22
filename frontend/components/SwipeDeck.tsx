'use client';

import Link from 'next/link';
import { useCallback, useEffect, useRef, useState } from 'react';
import { DetailSheet } from '@/components/DetailSheet';
import { MatchMoment } from '@/components/MatchMoment';
import { ApiError } from '@/lib/api';
import type { Card, Match, SwipeResponse } from '@/lib/types';

export function SwipeDeck({
  cards,
  interestLabel,
  onSwipe,
}: {
  cards: Card[];
  interestLabel: string;
  onSwipe: (card: Card, direction: 'like' | 'pass') => Promise<SwipeResponse>;
}) {
  const [index, setIndex] = useState(0);
  const [x, setX] = useState(0);
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState('');
  const [match, setMatch] = useState<Match | null>(null);
  const [detail, setDetail] = useState(false);
  const origin = useRef(0);
  const lock = useRef(false);
  const draggingRef = useRef(false);
  const card = cards[index];

  const commit = useCallback(
    async (direction: 'like' | 'pass') => {
      if (!card || lock.current) return;
      lock.current = true;
      setDetail(false);
      setError('');
      setDragging(false);
      setX(direction === 'like' ? 460 : -460);
      try {
        const result = await onSwipe(card, direction);
        await new Promise((resolve) => setTimeout(resolve, 200));
        if (result.matched && result.match) {
          setMatch(result.match);
        } else {
          setIndex((current) => current + 1);
          setX(0);
        }
      } catch (err) {
        setX(0);
        if (err instanceof ApiError && err.status === 409) {
          setIndex((current) => current + 1);
        } else {
          setError(err instanceof ApiError ? err.message : 'Could not save that response.');
        }
      } finally {
        lock.current = false;
      }
    },
    [card, onSwipe],
  );

  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (!card || match || detail) return;
      if (event.key === 'ArrowLeft') void commit('pass');
      if (event.key === 'ArrowRight') void commit('like');
    }
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [card, match, detail, commit]);

  if (!card && !match) {
    return (
      <div className="empty-card">
        <p className="eyebrow">That's everyone</p>
        <h1 className="display">No one new right now.</h1>
        <p>When someone in Dublin finishes a profile, they will show up here.</p>
        <Link href="/matches" className="btn btn-clay">
          See matches
        </Link>
      </div>
    );
  }

  const amount = Math.min(Math.abs(x) / 110, 1);

  return (
    <div className="deck">
      {cards[index + 1] ? <div className="peek" aria-hidden="true" /> : null}
      {card ? (
        <article
          className="person-card"
          style={{
            transform: `translateX(${x}px) rotate(${x / 22}deg)`,
            transition: dragging ? 'none' : 'transform 200ms ease',
          }}
          onPointerDown={(event) => {
            if ((event.target as HTMLElement).closest('button, a')) return;
            origin.current = event.clientX;
            draggingRef.current = true;
            setDragging(true);
            event.currentTarget.setPointerCapture(event.pointerId);
          }}
          onPointerMove={(event) => {
            if (!draggingRef.current) return;
            setX(event.clientX - origin.current);
          }}
          onPointerUp={(event) => {
            if (!draggingRef.current) return;
            draggingRef.current = false;
            const delta = event.clientX - origin.current;
            setDragging(false);
            if (delta > 96) void commit('like');
            else if (delta < -96) void commit('pass');
            else setX(0);
          }}
          onPointerCancel={() => {
            draggingRef.current = false;
            setDragging(false);
            setX(0);
          }}
        >
          <div className="photo">
            {card.photo_url ? <img src={card.photo_url} alt="" /> : <div className="portrait-fallback">{card.display_name.slice(0, 1)}</div>}
            <span className="stamp like" style={{ opacity: x > 0 ? amount : 0 }}>
              {interestLabel}
            </span>
            <span className="stamp pass" style={{ opacity: x < 0 ? amount : 0 }}>
              Pass
            </span>
          </div>
          <div className="card-copy">
            <p className="eyebrow">{card.kicker}</p>
            <h2 className="display">{card.display_name}</h2>
            {card.headline ? <p className="headline">{card.headline}</p> : null}
            {card.highlights.length ? (
              <ul className="highlights">
                {card.highlights.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            ) : null}
            {card.bio ? <p className="clamp">{card.bio}</p> : null}
            <button type="button" className="text-btn" onClick={() => setDetail(true)}>
              Full profile
            </button>
          </div>
        </article>
      ) : null}
      {card ? (
        <div className="dock">
          <button type="button" className="btn btn-pass" onClick={() => void commit('pass')}>
            Pass
          </button>
          <button type="button" className="btn btn-interest" onClick={() => void commit('like')}>
            {interestLabel}
          </button>
        </div>
      ) : null}
      {error ? (
        <p className="alert" role="alert">
          {error}
        </p>
      ) : null}
      {detail && card ? (
        <DetailSheet
          card={card}
          interestLabel={interestLabel}
          onClose={() => setDetail(false)}
          onPass={() => void commit('pass')}
          onLike={() => void commit('like')}
        />
      ) : null}
      {match ? (
        <MatchMoment
          match={match}
          onClose={() => {
            setMatch(null);
            setX(0);
            setIndex((current) => current + 1);
          }}
        />
      ) : null}
    </div>
  );
}
