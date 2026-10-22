'use client';

import { useState } from 'react';
import { AreaPicker, Check, ChildEditor, ChipSet, Field, LanguageEditor, PhotoField } from '@/components/controls';
import { WizardFrame } from '@/components/WizardFrame';
import { ApiError, api } from '@/lib/api';
import { FAMILY_STEP, type FamilyForm, familyIssue, toFamilyPayload } from '@/lib/profileForm';
import type { Meta, ProfileResponse } from '@/lib/types';

const STEPS = [
  {
    title: 'Your family',
    lede: 'Who you are, and where in Dublin the care happens.',
  },
  {
    title: 'The children',
    lede: 'How many, and how old. Add one row per child.',
  },
  {
    title: 'When you need care',
    lede: 'Days, hours, and when you want to start.',
  },
  {
    title: 'The arrangement',
    lede: 'Live-in or live-out, the duties, and the room if there is one.',
  },
  {
    title: 'Pay and a short note',
    lede: 'Put the number you would actually offer.',
  },
];

export function FamilyWizard({
  meta,
  initial,
  onSaved,
}: {
  meta: Meta;
  initial: FamilyForm;
  onSaved: (result: ProfileResponse) => void;
}) {
  const [form, setForm] = useState(initial);
  const [step, setStep] = useState(0);
  const [error, setError] = useState('');
  const [missing, setMissing] = useState<string[]>([]);
  const [saving, setSaving] = useState(false);

  function patch(partial: Partial<FamilyForm>) {
    setForm((current) => ({ ...current, ...partial }));
  }

  async function persist(nextStep: number | null, finish: boolean) {
    if (nextStep !== null && nextStep > step) {
      const problem = familyIssue(form, step);
      if (problem) {
        setError(problem);
        return;
      }
    }
    if (finish) {
      const problem = familyIssue(form, 'all');
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
        body: JSON.stringify(toFamilyPayload(form)),
      });
      if (finish) {
        if (!result.complete) {
          setMissing(result.missing.map((item) => item.label));
          const key = result.missing[0]?.key;
          if (key && key in FAMILY_STEP) setStep(FAMILY_STEP[key]);
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
  const needsRoom = form.arrangement === 'live_in' || form.arrangement === 'either';

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
          <Field label="Name" hint="Brennan family, or your own name.">
            <input value={form.display_name} onChange={(event) => patch({ display_name: event.target.value })} />
          </Field>
          <Field label="WhatsApp">
            <input value={form.whatsapp} inputMode="tel" onChange={(event) => patch({ whatsapp: event.target.value })} />
          </Field>
          <Field label="Where do you need care?" hint="Dublin areas for now.">
            <AreaPicker groups={meta.areas} selected={form.area ? [form.area] : []} multiple={false} onChange={(next) => patch({ area: next[0] ?? '' })} />
          </Field>
          <Field label="Household" hint="Optional.">
            <ChipSet
              options={meta.households}
              value={form.household ? [form.household] : []}
              single
              onChange={(next) => patch({ household: next[0] ?? '' })}
            />
          </Field>
        </>
      ) : null}
      {step === 1 ? (
        <>
          <ChildEditor rows={form.children} onChange={(children) => patch({ children })} />
          <p className="quiet">Years, and months if they are little. A 14-month-old is 1 year and 2 months.</p>
        </>
      ) : null}
      {step === 2 ? (
        <>
          <Field label="When do you need care?">
            <textarea value={form.schedule_notes} onChange={(event) => patch({ schedule_notes: event.target.value })} />
          </Field>
          <Field label="Days">
            <ChipSet options={meta.days} value={form.days_needed} onChange={(days_needed) => patch({ days_needed })} />
          </Field>
          <Field label="Times of day">
            <ChipSet options={meta.care_windows} value={form.care_windows} onChange={(care_windows) => patch({ care_windows })} />
          </Field>
          <Field label="Hours a week">
            <input
              inputMode="numeric"
              value={form.hours_per_week}
              onChange={(event) => patch({ hours_per_week: event.target.value.replace(/\D/g, '').slice(0, 2) })}
            />
          </Field>
          <Field label="When do you want to start?">
            <ChipSet
              options={meta.start_timings}
              value={form.start_timing ? [form.start_timing] : []}
              single
              onChange={(next) => patch({ start_timing: next[0] ?? '' })}
            />
          </Field>
          <Field label="How many months?" hint="Optional.">
            <input
              inputMode="numeric"
              value={form.duration_months}
              onChange={(event) => patch({ duration_months: event.target.value.replace(/\D/g, '').slice(0, 2) })}
            />
          </Field>
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
          <Field label="Duties">
            <ChipSet options={meta.duties} value={form.duties} onChange={(duties) => patch({ duties })} />
          </Field>
          <Field label="Languages at home">
            <LanguageEditor
              rows={form.languages_at_home}
              languages={meta.languages}
              levels={meta.levels}
              onChange={(languages_at_home) => patch({ languages_at_home })}
            />
          </Field>
          <Check label="There is a pet" checked={form.has_pets} onChange={(has_pets) => patch({ has_pets })} />
          {form.has_pets ? (
            <Field label="About the pet">
              <input value={form.pet_notes} onChange={(event) => patch({ pet_notes: event.target.value })} />
            </Field>
          ) : null}
          {needsRoom ? (
            <>
              <Check label="Own room" checked={form.own_room} onChange={(own_room) => patch({ own_room })} />
              <Field label="The room and the area" hint="Au pairs in Ireland expect their own room if they live in.">
                <textarea value={form.accommodation_notes} onChange={(event) => patch({ accommodation_notes: event.target.value })} />
              </Field>
            </>
          ) : null}
        </>
      ) : null}
      {step === 4 ? (
        <>
          <Field label="How will you pay?" hint="Weekly pocket money is the usual live-in offer. Evenings and babysitting are usually hourly.">
            <ChipSet
              options={meta.pay_basis}
              value={form.pay_basis ? [form.pay_basis] : []}
              single
              onChange={(next) => patch({ pay_basis: next[0] ?? '' })}
            />
          </Field>
          <Field label="Amount, euro">
            <input
              inputMode="numeric"
              value={form.pay_amount}
              onChange={(event) => patch({ pay_amount: event.target.value.replace(/\D/g, '').slice(0, 4) })}
            />
          </Field>
          <Check label="Open to negotiating" checked={form.pay_negotiable} onChange={(pay_negotiable) => patch({ pay_negotiable })} />
          <Field label="A note about your family">
            <textarea value={form.bio} maxLength={1500} onChange={(event) => patch({ bio: event.target.value })} />
          </Field>
        </>
      ) : null}
    </WizardFrame>
  );
}
