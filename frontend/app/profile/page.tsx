'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { AppShell } from '@/components/AppShell';
import { ProfileDetails } from '@/components/ProfileDetails';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth';
import type { CandidateProfile, FamilyProfile, ProfileResponse } from '@/lib/types';

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const [data, setData] = useState<ProfileResponse | null>(null);

  useEffect(() => {
    api<ProfileResponse>('/profile')
      .then(setData)
      .catch(() => setData(null));
  }, []);

  const profile = data?.profile as (CandidateProfile & FamilyProfile) | undefined;
  const whatsapp = profile?.whatsapp ?? '';

  return (
    <AppShell>
      <div className="page">
        <p className="eyebrow">Your profile</p>
        <h1 className="display">{data?.card.display_name || 'Your profile'}</h1>
        <p className="quiet">{user?.email}</p>
        {data?.card.photo_url ? <img className="profile-photo" src={data.card.photo_url} alt="" /> : null}
        {data?.card.bio ? <p>{data.card.bio}</p> : null}
        {whatsapp ? (
          <p>
            <strong>Your WhatsApp.</strong> {whatsapp}. Other people see this only after you match.
          </p>
        ) : null}
        {data ? <ProfileDetails card={data.card} /> : <p>Loading your profile</p>}
        <div className="stack tight">
          <Link className="btn btn-clay" href="/onboarding">
            Edit profile
          </Link>
          <button type="button" className="btn btn-ghost" onClick={() => void logout()}>
            Sign out
          </button>
        </div>
      </div>
    </AppShell>
  );
}
