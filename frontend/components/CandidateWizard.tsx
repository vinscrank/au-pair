'use client';

import { useState } from 'react';
import { AreaPicker, Check, ChipSet, Field, LanguageEditor, PhotoField } from '@/components/controls';
import { WizardFrame } from '@/components/WizardFrame';
import { ApiError, api } from '@/lib/api';
import {
  CANDIDATE_STEP,
  type CandidateForm,
  candidateIssue,
  toCandidatePayload,
} from '@/lib/profileForm';
import type { Meta, ProfileResponse } from '@/lib/types';

const STEPS = [
  {
    title: 'About you',
    lede: 'The basics a family looks for before they read on.',
  },
  {
    title: 'Languages',
    lede: 'Include English, and say how comfortable you are.',
  },
  {
    title: 'Experience',
    lede: 'Ages you have actually minded. A formal certificate can wait.',
  },
  {
    title: 'The work',
    lede: 'Where you can be, and what you will do.',
  },
  {
    title: 'When',
    lede: 'Hours, days, and when you can start.',
  },
  {
    title: 'Pay and a short note',
    lede: 'Say what you are hoping for. Families put a number too.',
  },
];

export function CandidateWizard({
  meta,
  initial,
  onSaved,
}: {
  meta: Meta;
  initial: CandidateForm;
  onSaved: (result: ProfileResponse) => void;
}) {
  const [form, setForm] = useState(initial);
  const [step, setStep] = useState(0);
  const [error, setError] = useState('');
  const [missing, setMissing] = useState<string[]>([]);
  const [saving, setSaving] = useState(false);

  function patch(partial: Partial<CandidateForm>) {
    setForm((current) => ({ ...current, ...partial }));
  }

  async function persist(nextStep: number | null, finish: boolean) {
    if (nextStep !== null && nextStep > step) {
      const problem = candidateIssue(form, step);
      if (problem) {
        setError(problem);
        return;
      }
    }
    if (finish) {
      const problem = candidateIssue(form, 'all');
      if (problem) {
        setError(problem);
        return;
      }
    }
    setSaving(true);
    setError('');
    try {
      const result = await api<ProfileResponse>('/profile', {
        method: 'PUT',
        body: JSON.stringify(toCandidatePayload(form)),
      });
      if (finish) {
        if (!result.complete) {
          setMissing(result.missing.map((item) => item.label));
          const key = result.missing[0]?.key;
          if (key && key in CANDIDATE_STEP) setStep(CANDIDATE_STEP[key]);
          return;
        }
        onSaved(result);
        return;
      }
      if (nextStep !== null) setStep(nextStep);
      setMissing([]);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save just now.');
    } finally {
      setSaving(false);
    }
  }

  const current = STEPS[step];

  return (
    <WizardFrame
      step={step}
      count={STEPS.length}
      title={current.title}
      lede={current.lede}
      error={error}
      missing={missing}
      saving={saving}
      isLast={step === STEPS.length - 1}
      onBack={() => void persist(step - 1, false)}
      onNext={() => void persist(step === STEPS.length - 1 ? null : step + 1, step === STEPS.length - 1)}
    >
      {step === 0 ? (
        <>
          <PhotoField url={form.photo_url} onUploaded={(photo_url) => patch({ photo_url })} />
          <Field label="Name">
            <input value={form.display_name} onChange={(event) => patch({ display_name: event.target.value })} />
          </Field>
          <Field label="WhatsApp" hint="Include the country code if it is not an Irish mobile.">
            <input value={form.whatsapp} inputMode="tel" onChange={(event) => patch({ whatsapp: event.target.value })} />
          </Field>
          <Field label="Age">
            <input inputMode="numeric" value={form.age} onChange={(event) => patch({ age: event.target.value.replace(/\D/g, '').slice(0, 2) })} />
          </Field>
          <Field label="Gender" hint="Optional.">
            <ChipSet options={meta.genders} value={form.gender ? [form.gender] : []} single onChange={(next) => patch({ gender: next[0] ?? '' })} />
          </Field>
          <Field label="Nationality" hint="Italian, Irish, Polish, French...">
            <input value={form.nationality} onChange={(event) => patch({ nationality: event.target.value })} />
          </Field>
          <Field label="Where are you based now?">
            <input value={form.based_in} onChange={(event) => patch({ based_in: event.target.value })} placeholder="Drumcondra, or still in Lyon" />
          </Field>
        </>
      ) : null}
      {step === 1 ? (
        <LanguageEditor rows={form.languages} languages={meta.languages} levels={meta.levels} onChange={(languages) => patch({ languages })} />
      ) : null}
      {step === 2 ? (
        <>
          <Field label="Years minding children" hint="Use 0 if you have only helped family so far.">
            <input
              inputMode="numeric"
              value={form.experience_years}
              onChange={(event) => patch({ experience_years: event.target.value.replace(/\D/g, '').slice(0, 2) })}
            />
          </Field>
          <Field label="Ages you have looked after">
            <ChipSet
              options={meta.age_bands}
              value={form.experience_age_bands}
              onChange={(experience_age_bands) => patch({ experience_age_bands })}
            />
          </Field>
          <Field label="A line on that experience" hint="Optional.">
            <textarea value={form.experience_summary} onChange={(event) => patch({ experience_summary: event.target.value })} />
          </Field>
          <Field label="Qualification" hint="QQI, Montessori, paediatric first aid. Optional.">
            <input value={form.qualification} onChange={(event) => patch({ qualification: event.target.value })} />
          </Field>
          <Check label="First aid" checked={form.first_aid} onChange={(first_aid) => patch({ first_aid })} />
          <Check
            label="Garda vetting"
            hint="Say yes only if you hold it. Mobijob does not check the disclosure."
            checked={form.garda_vetting}
            onChange={(garda_vetting) => patch({ garda_vetting })}
          />
          <Check label="References available" checked={form.has_references} onChange={(has_references) => patch({ has_references })} />
          <Check
            label="Experience with special needs"
            checked={form.special_needs_experience}
            onChange={(special_needs_experience) => patch({ special_needs_experience })}
          />
        </>
      ) : null}
      {step === 3 ? (
        <>
          <Field label="Live-in or live-out">
            <ChipSet
              options={meta.arrangements}
              value={form.arrangement ? [form.arrangement] : []}
              single
              onChange={(next) => patch({ arrangement: next[0] ?? '' })}
            />
          </Field>
          <Field label="Dublin areas you can work" hint="Up to 8. Ireland beyond Dublin can come later.">
            <AreaPicker groups={meta.areas} selected={form.areas} multiple onChange={(areas) => patch({ areas })} />
          </Field>
          <Field label="Where you can mind">
            <ChipSet options={meta.minds_in} value={form.minds_in} onChange={(minds_in) => patch({ minds_in })} />
          </Field>
          <Field label="Duties you will do">
            <ChipSet options={meta.duties} value={form.duties} onChange={(duties) => patch({ duties })} />
          </Field>
          <Field label="Smoking">
            <ChipSet
              options={[
                { value: 'no', label: 'Non-smoker' },
                { value: 'yes', label: 'Smoker' },
              ]}
              value={form.smoker ? [form.smoker] : []}
              single
              onChange={(next) => patch({ smoker: (next[0] as 'yes' | 'no') ?? '' })}
            />
          </Field>
          <Check label="Comfortable with pets" checked={form.comfortable_with_pets} onChange={(comfortable_with_pets) => patch({ comfortable_with_pets })} />
          <Check label="Full driving licence" checked={form.has_driving_licence} onChange={(has_driving_licence) => patch({ has_driving_licence })} />
          <Check label="Own car" checked={form.has_own_car} onChange={(has_own_car) => patch({ has_own_car })} />
          <Check label="EU passport" checked={form.eu_passport} onChange={(eu_passport) => patch({ eu_passport })} />
        </>
      ) : null}
      {step === 4 ? (
        <>
          <Field label="When are you available?">
            <textarea value={form.schedule_notes} onChange={(event) => patch({ schedule_notes: event.target.value })} />
          </Field>
          <Field label="Days" hint="Optional, if the note above is clear.">
            <ChipSet options={meta.days} value={form.days_available} onChange={(days_available) => patch({ days_available })} />
          </Field>
          <Field label="Hours a week" hint="Optional.">
            <input
              inputMode="numeric"
              value={form.hours_per_week}
              onChange={(event) => patch({ hours_per_week: event.target.value.replace(/\D/g, '').slice(0, 2) })}
            />
          </Field>
          <Check
            label="Available at short notice"
            checked={form.available_short_notice}
            onChange={(available_short_notice) => patch({ available_short_notice })}
          />
          <Field label="When can you start?">
            <ChipSet
              options={meta.start_timings}
              value={form.start_timing ? [form.start_timing] : []}
              single
              onChange={(next) => patch({ start_timing: next[0] ?? '' })}
            />
          </Field>
          <Field label="How many months could you stay?" hint="Optional. Common for au pairs.">
            <input
              inputMode="numeric"
              value={form.duration_months}
              onChange={(event) => patch({ duration_months: event.target.value.replace(/\D/g, '').slice(0, 2) })}
            />
          </Field>
        </>
      ) : null}
      {step === 5 ? (
        <>
          <Field label="How should pay be described?" hint="Live-in ads in Dublin usually show weekly pocket money. Babysitting is usually hourly.">
            <ChipSet
              options={meta.pay_basis}
              value={form.pay_basis ? [form.pay_basis] : []}
              single
              onChange={(next) => patch({ pay_basis: next[0] ?? '' })}
            />
          </Field>
          <div className="pair">
            <Field label="From, euro">
              <input inputMode="numeric" value={form.pay_min} onChange={(event) => patch({ pay_min: event.target.value.replace(/\D/g, '').slice(0, 4) })} />
            </Field>
            <Field label="Up to, optional">
              <input inputMode="numeric" value={form.pay_max} onChange={(event) => patch({ pay_max: event.target.value.replace(/\D/g, '').slice(0, 4) })} />
            </Field>
          </div>
          <Check label="Pay is negotiable" checked={form.pay_negotiable} onChange={(pay_negotiable) => patch({ pay_negotiable })} />
          <Field label="Short bio">
            <textarea value={form.bio} maxLength={1500} onChange={(event) => patch({ bio: event.target.value })} />
          </Field>
        </>
      ) : null}
    </WizardFrame>
  );
}
