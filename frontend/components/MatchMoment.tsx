'use client';

import { whatsappHref } from '@/lib/phone';
import type { Match } from '@/lib/types';

export function MatchMoment({ match, onClose }: { match: Match; onClose: () => void }) {
  const whatsapp = match.contact.available && match.contact.value ? match.contact.value : null;
  return (
    <div className="match" role="dialog" aria-modal="true" aria-labelledby="match-title">
      <p className="eyebrow light">Mutual match</p>
      <h1 id="match-title" className="display">
        You both said yes.
      </h1>
      {match.card.photo_url ? <img src={match.card.photo_url} alt="" /> : null}
      <p className="match-name">{match.card.display_name}</p>
      {match.card.headline ? <p className="match-line">{match.card.headline}</p> : null}
      {whatsapp ? (
        <a className="btn btn-clay" href={whatsappHref(whatsapp)} target="_blank" rel="noreferrer">
          Message on WhatsApp
        </a>
      ) : (
        <p className="match-line">WhatsApp is not open on this match yet.</p>
      )}
      <button type="button" className="btn btn-ghost light" onClick={onClose}>
        Keep looking
      </button>
    </div>
  );
}
