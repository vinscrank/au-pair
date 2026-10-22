'use client';

import { ProfileDetails } from '@/components/ProfileDetails';
import { whatsappHref } from '@/lib/phone';
import type { Card, Contact } from '@/lib/types';

export function DetailSheet({
  card,
  contact,
  interestLabel,
  onClose,
  onLike,
  onPass,
}: {
  card: Card;
  contact?: Contact | null;
  interestLabel?: string;
  onClose: () => void;
  onLike?: () => void;
  onPass?: () => void;
}) {
  const whatsapp = contact?.available && contact.value ? contact.value : null;
  return (
    <div className="sheet-back" onClick={onClose}>
      <div
        className="sheet"
        role="dialog"
        aria-modal="true"
        aria-label={card.display_name}
        onClick={(event) => event.stopPropagation()}
      >
        <button type="button" className="text-btn" onClick={onClose}>
          Close
        </button>
        <div className="sheet-photo">{card.photo_url ? <img src={card.photo_url} alt="" /> : null}</div>
        <p className="eyebrow">{card.kicker}</p>
        <h2 className="display">{card.display_name}</h2>
        {card.headline ? <p className="headline">{card.headline}</p> : null}
        {card.bio ? <p className="bio">{card.bio}</p> : null}
        <ProfileDetails card={card} />
        {contact ? (
          whatsapp ? (
            <a className="btn btn-clay" href={whatsappHref(whatsapp)} target="_blank" rel="noreferrer">
              Message on WhatsApp
            </a>
          ) : (
            <p className="quiet">WhatsApp is not open on this match yet.</p>
          )
        ) : null}
        {onLike && onPass ? (
          <div className="dock">
            <button type="button" className="btn btn-pass" onClick={onPass}>
              Pass
            </button>
            <button type="button" className="btn btn-interest" onClick={onLike}>
              {interestLabel}
            </button>
          </div>
        ) : null}
      </div>
    </div>
  );
}
