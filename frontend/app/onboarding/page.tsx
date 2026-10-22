'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { flushSync } from 'react-dom';
import { AppShell } from '@/components/AppShell';
import { CandidateWizard } from '@/components/CandidateWizard';
import { FamilyWizard } from '@/components/FamilyWizard';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth';
import { candidateFromProfile, familyFromProfile } from '@/lib/profileForm';
import type { CandidateProfile, FamilyProfile, Me, Meta, ProfileResponse } from '@/lib/types';

export default function OnboardingPage() {
  const { user, adopt } = useAuth();
  const router = useRouter();
  const [meta, setMeta] = useState<Meta | null>(null);
  const [profile, setProfile] = useState<ProfileResponse | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([api<Meta>('/meta'), api<ProfileResponse>('/profile')])
      .then(([nextMeta, nextProfile]) => {
        setMeta(nextMeta);
        setProfile(nextProfile);
      })
      .catch(() => setError('Could not open your profile.'));
  }, []);

  async function onSaved() {
    const me = await api<Me>('/auth/me');
    flushSync(() => adopt(me));
    router.push('/discover');
  }

  return (
    <AppShell variant="plain">
      {error ? (
        <p className="alert page-pad" role="alert">
          {error}
        </p>
      ) : null}
      {!meta || !profile || !user ? (
        <p className="page-pad">Loading your profile</p>
      ) : user.role === 'family' ? (
        <FamilyWizard meta={meta} initial={familyFromProfile(profile.profile as FamilyProfile)} onSaved={onSaved} />
      ) : (
        <CandidateWizard meta={meta} initial={candidateFromProfile(profile.profile as CandidateProfile)} onSaved={onSaved} />
      )}
    </AppShell>
  );
}
