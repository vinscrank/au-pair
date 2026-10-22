import type { CandidateProfile, ChildRow, FamilyProfile, LanguageRow } from '@/lib/types';

export type CandidateForm = {
  display_name: string;
  whatsapp: string;
  photo_url: string;
  age: string;
  gender: string;
  nationality: string;
  based_in: string;
  languages: LanguageRow[];
  experience_years: string;
  experience_age_bands: string[];
  experience_summary: string;
  qualification: string;
  first_aid: boolean;
  garda_vetting: boolean;
  has_references: boolean;
  smoker: '' | 'yes' | 'no';
  comfortable_with_pets: boolean;
  has_driving_licence: boolean;
  has_own_car: boolean;
  eu_passport: boolean;
  special_needs_experience: boolean;
  duties: string[];
  arrangement: string;
  areas: string[];
  minds_in: string[];
  days_available: string[];
  hours_per_week: string;
  schedule_notes: string;
  available_short_notice: boolean;
  start_timing: string;
  duration_months: string;
  pay_basis: string;
  pay_min: string;
  pay_max: string;
  pay_negotiable: boolean;
  bio: string;
};

export type FamilyForm = {
  display_name: string;
  whatsapp: string;
  photo_url: string;
  area: string;
  children: ChildRow[];
  schedule_notes: string;
  days_needed: string[];
  hours_per_week: string;
  care_windows: string[];
  start_timing: string;
  duration_months: string;
  arrangement: string;
  duties: string[];
  languages_at_home: LanguageRow[];
  household: string;
  has_pets: boolean;
  pet_notes: string;
  own_room: boolean;
  accommodation_notes: string;
  pay_basis: string;
  pay_amount: string;
  pay_negotiable: boolean;
  bio: string;
};

export const CANDIDATE_STEP: Record<string, number> = {
  display_name: 0,
  whatsapp: 0,
  photo_url: 0,
  age: 0,
  nationality: 0,
  based_in: 0,
  gender: 0,
  languages: 1,
  experience_years: 2,
  experience_age_bands: 2,
  experience_summary: 2,
  qualification: 2,
  arrangement: 3,
  areas: 3,
  minds_in: 3,
  duties: 3,
  smoker: 3,
  schedule_notes: 4,
  start_timing: 4,
  hours_per_week: 4,
  pay_basis: 5,
  pay_min: 5,
  pay_max: 5,
  bio: 5,
};

export const FAMILY_STEP: Record<string, number> = {
  display_name: 0,
  whatsapp: 0,
  photo_url: 0,
  area: 0,
  children: 1,
  schedule_notes: 2,
  hours_per_week: 2,
  start_timing: 2,
  days_needed: 2,
  care_windows: 2,
  arrangement: 3,
  duties: 3,
  languages_at_home: 3,
  own_room: 3,
  accommodation_notes: 3,
  pay_basis: 4,
  pay_amount: 4,
  bio: 4,
};

function blankLanguage(): LanguageRow {
  return { language: '', level: '' };
}

function blankChild(): ChildRow {
  return { age_years: '', age_months: '' };
}

function textNumber(value: number | null | undefined): string {
  return value == null ? '' : String(value);
}

export function emptyCandidate(): CandidateForm {
  return {
    display_name: '',
    whatsapp: '',
    photo_url: '',
    age: '',
    gender: '',
    nationality: '',
    based_in: '',
    languages: [blankLanguage()],
    experience_years: '',
    experience_age_bands: [],
    experience_summary: '',
    qualification: '',
    first_aid: false,
    garda_vetting: false,
    has_references: false,
    smoker: '',
    comfortable_with_pets: false,
    has_driving_licence: false,
    has_own_car: false,
    eu_passport: false,
    special_needs_experience: false,
    duties: [],
    arrangement: '',
    areas: [],
    minds_in: [],
    days_available: [],
    hours_per_week: '',
    schedule_notes: '',
    available_short_notice: false,
    start_timing: '',
    duration_months: '',
    pay_basis: '',
    pay_min: '',
    pay_max: '',
    pay_negotiable: false,
    bio: '',
  };
}

export function emptyFamily(): FamilyForm {
  return {
    display_name: '',
    whatsapp: '',
    photo_url: '',
    area: '',
    children: [blankChild()],
    schedule_notes: '',
    days_needed: [],
    hours_per_week: '',
    care_windows: [],
    start_timing: '',
    duration_months: '',
    arrangement: '',
    duties: [],
    languages_at_home: [blankLanguage()],
    household: '',
    has_pets: false,
    pet_notes: '',
    own_room: false,
    accommodation_notes: '',
    pay_basis: '',
    pay_amount: '',
    pay_negotiable: false,
    bio: '',
  };
}

export function candidateFromProfile(profile: CandidateProfile): CandidateForm {
  return {
    ...emptyCandidate(),
    ...profile,
    age: textNumber(profile.age),
    experience_years: textNumber(profile.experience_years),
    hours_per_week: textNumber(profile.hours_per_week),
    duration_months: textNumber(profile.duration_months),
    pay_min: textNumber(profile.pay_min),
    pay_max: textNumber(profile.pay_max),
    smoker: profile.smoker == null ? '' : profile.smoker ? 'yes' : 'no',
    languages: profile.languages?.length ? profile.languages : [blankLanguage()],
    experience_age_bands: profile.experience_age_bands ?? [],
    duties: profile.duties ?? [],
    areas: profile.areas ?? [],
    minds_in: profile.minds_in ?? [],
    days_available: profile.days_available ?? [],
  };
}

export function familyFromProfile(profile: FamilyProfile): FamilyForm {
  const children = (profile.children ?? [])
    .filter((child) => child.age_years != null)
    .map((child) => ({
      age_years: String(child.age_years),
      age_months: child.age_months == null ? '' : String(child.age_months),
    }));
  return {
    ...emptyFamily(),
    display_name: profile.display_name ?? '',
    whatsapp: profile.whatsapp ?? '',
    photo_url: profile.photo_url ?? '',
    area: profile.area ?? '',
    children: children.length ? children : [blankChild()],
    schedule_notes: profile.schedule_notes ?? '',
    days_needed: profile.days_needed ?? [],
    hours_per_week: textNumber(profile.hours_per_week),
    care_windows: profile.care_windows ?? [],
    start_timing: profile.start_timing ?? '',
    duration_months: textNumber(profile.duration_months),
    arrangement: profile.arrangement ?? '',
    duties: profile.duties ?? [],
    languages_at_home: profile.languages_at_home?.length ? profile.languages_at_home : [blankLanguage()],
    household: profile.household ?? '',
    has_pets: Boolean(profile.has_pets),
    pet_notes: profile.pet_notes ?? '',
    own_room: Boolean(profile.own_room),
    accommodation_notes: profile.accommodation_notes ?? '',
    pay_basis: profile.pay_basis ?? '',
    pay_amount: textNumber(profile.pay_amount),
    pay_negotiable: Boolean(profile.pay_negotiable),
    bio: profile.bio ?? '',
  };
}

function whole(value: string): number | null {
  if (!/^\d+$/.test(value.trim())) return null;
  return Number(value.trim());
}

function phoneOk(value: string): boolean {
  return value.replace(/\D/g, '').length >= 7;
}

function languageIssue(rows: LanguageRow[], emptyMessage: string): string | null {
  const partial = rows.some((row) => (row.language && !row.level) || (!row.language && row.level));
  if (partial) return 'Finish each language row, or clear it.';
  if (!rows.some((row) => row.language && row.level)) return emptyMessage;
  return null;
}

function optionalWhole(value: string, label: string, max: number): string | null {
  if (!value.trim()) return null;
  const parsed = whole(value);
  if (parsed === null || parsed < 1 || parsed > max) return `${label} should be a whole number up to ${max}.`;
  return null;
}

export function candidateIssue(form: CandidateForm, step: number | 'all'): string | null {
  const checks = [
    () => {
      if (!form.photo_url) return 'Add a photo to continue.';
      if (form.display_name.trim().length < 2) return 'Add your name.';
      if (!phoneOk(form.whatsapp)) return 'Add a WhatsApp number, with the country code if you are outside Ireland.';
      const age = whole(form.age);
      if (age === null || age < 18 || age > 75) return 'Add your age. Mobijob is for people 18 and over.';
      if (form.nationality.trim().length < 2) return 'Add your nationality.';
      if (form.based_in.trim().length < 2) return 'Say where you are based now.';
      return null;
    },
    () => languageIssue(form.languages, 'Add at least one language and a level.'),
    () => {
      const years = whole(form.experience_years);
      if (years === null || years > 60) return 'Add how many years you have minded children. Use 0 if this is new for you.';
      if (form.experience_age_bands.length === 0) return 'Choose the ages you have looked after.';
      return null;
    },
    () => {
      if (!form.arrangement) return 'Choose live-in, live-out, or either.';
      if (form.areas.length === 0) return 'Choose at least one Dublin area.';
      if (form.minds_in.length === 0) return 'Say where you can mind children.';
      if (form.duties.length === 0) return 'Choose at least one duty you will do.';
      if (!form.smoker) return 'Say whether you smoke.';
      return null;
    },
    () => {
      if (form.schedule_notes.trim().length < 10) return 'Describe when you are available, in a sentence or two.';
      if (!form.start_timing) return 'Choose when you can start.';
      return optionalWhole(form.hours_per_week, 'Hours a week', 80) || optionalWhole(form.duration_months, 'Duration', 36);
    },
    () => {
      if (!form.pay_basis) return 'Choose how you want to be paid.';
      if (!form.pay_negotiable) {
        const amount = whole(form.pay_min);
        if (amount === null || amount <= 0) return 'Add the pay you are hoping for, or mark it as negotiable.';
      } else if (form.pay_min.trim()) {
        const amount = whole(form.pay_min);
        if (amount === null) return 'Pay should be a whole number of euro.';
      }
      if (form.pay_min.trim() && form.pay_max.trim()) {
        const min = whole(form.pay_min);
        const max = whole(form.pay_max);
        if (min === null || max === null || max < min) return 'The top of the pay range should be at least the bottom.';
      }
      if (form.bio.trim().length < 20) return 'Write a short bio, at least a sentence or two.';
      return null;
    },
  ];
  const indexes = step === 'all' ? checks.map((_, index) => index) : [step];
  for (const index of indexes) {
    const message = checks[index]();
    if (message) return message;
  }
  return null;
}

export function familyIssue(form: FamilyForm, step: number | 'all'): string | null {
  const checks = [
    () => {
      if (!form.photo_url) return 'Add a photo of you or your home.';
      if (form.display_name.trim().length < 2) return 'Add a name families will recognise, such as Brennan family.';
      if (!phoneOk(form.whatsapp)) return 'Add a WhatsApp number.';
      if (!form.area) return 'Choose where you need care.';
      return null;
    },
    () => {
      const filled = form.children.filter((child) => child.age_years !== '' || child.age_months !== '');
      if (filled.length === 0) return "Add each child's age. Use 0 years for a baby under 1.";
      for (const child of filled) {
        const years = whole(child.age_years);
        if (years === null || years > 17) return "A child's age should be a whole number from 0 to 17.";
        if (child.age_months.trim()) {
          const months = whole(child.age_months);
          if (months === null || months > 11) return 'Months should be a whole number from 0 to 11.';
        }
      }
      return null;
    },
    () => {
      if (form.schedule_notes.trim().length < 10) return 'Describe when you need care: days, school runs, evenings.';
      const hours = whole(form.hours_per_week);
      if (hours === null || hours < 1 || hours > 80) return 'Add how many hours a week you need.';
      if (!form.start_timing) return 'Choose when you want to start.';
      return optionalWhole(form.duration_months, 'Duration', 36);
    },
    () => {
      if (!form.arrangement) return 'Choose live-in, live-out, or either.';
      if (form.duties.length === 0) return 'Choose the duties you need help with.';
      const languages = languageIssue(form.languages_at_home, 'Add at least one language you speak at home.');
      if (languages) return languages;
      if (form.arrangement === 'live_in' || form.arrangement === 'either') {
        if (!form.own_room) return 'Live-in needs a room of their own.';
        if (form.accommodation_notes.trim().length < 10) return 'Describe the room and how they would get around.';
      }
      return null;
    },
    () => {
      if (!form.pay_basis) return 'Choose how you will pay.';
      if (!form.pay_negotiable) {
        const amount = whole(form.pay_amount);
        if (amount === null || amount <= 0) return 'Add the pay you are offering, or mark it as negotiable.';
      }
      if (form.bio.trim().length < 20) return 'Write a short note about your family.';
      return null;
    },
  ];
  const indexes = step === 'all' ? checks.map((_, index) => index) : [step];
  for (const index of indexes) {
    const message = checks[index]();
    if (message) return message;
  }
  return null;
}

export function toCandidatePayload(form: CandidateForm) {
  return {
    display_name: form.display_name.trim(),
    whatsapp: form.whatsapp.trim(),
    photo_url: form.photo_url,
    age: whole(form.age),
    gender: form.gender,
    nationality: form.nationality.trim(),
    based_in: form.based_in.trim(),
    languages: form.languages.filter((row) => row.language && row.level),
    experience_years: whole(form.experience_years),
    experience_age_bands: form.experience_age_bands,
    experience_summary: form.experience_summary.trim(),
    qualification: form.qualification.trim(),
    first_aid: form.first_aid,
    garda_vetting: form.garda_vetting,
    has_references: form.has_references,
    smoker: form.smoker === '' ? null : form.smoker === 'yes',
    comfortable_with_pets: form.comfortable_with_pets,
    has_driving_licence: form.has_driving_licence,
    has_own_car: form.has_own_car,
    eu_passport: form.eu_passport,
    special_needs_experience: form.special_needs_experience,
    duties: form.duties,
    arrangement: form.arrangement,
    areas: form.areas,
    minds_in: form.minds_in,
    days_available: form.days_available,
    hours_per_week: form.hours_per_week.trim() ? whole(form.hours_per_week) : null,
    schedule_notes: form.schedule_notes.trim(),
    available_short_notice: form.available_short_notice,
    start_timing: form.start_timing,
    duration_months: form.duration_months.trim() ? whole(form.duration_months) : null,
    pay_basis: form.pay_basis,
    pay_min: form.pay_min.trim() ? whole(form.pay_min) : null,
    pay_max: form.pay_max.trim() ? whole(form.pay_max) : null,
    pay_negotiable: form.pay_negotiable,
    bio: form.bio.trim(),
  };
}

export function toFamilyPayload(form: FamilyForm) {
  return {
    display_name: form.display_name.trim(),
    whatsapp: form.whatsapp.trim(),
    photo_url: form.photo_url,
    area: form.area,
    children: form.children
      .filter((child) => child.age_years !== '')
      .map((child) => ({
        age_years: whole(child.age_years),
        age_months: child.age_months.trim() ? whole(child.age_months) : null,
      })),
    schedule_notes: form.schedule_notes.trim(),
    days_needed: form.days_needed,
    hours_per_week: form.hours_per_week.trim() ? whole(form.hours_per_week) : null,
    care_windows: form.care_windows,
    start_timing: form.start_timing,
    duration_months: form.duration_months.trim() ? whole(form.duration_months) : null,
    arrangement: form.arrangement,
    duties: form.duties,
    languages_at_home: form.languages_at_home.filter((row) => row.language && row.level),
    household: form.household,
    has_pets: form.has_pets,
    pet_notes: form.pet_notes.trim(),
    own_room: form.own_room,
    accommodation_notes: form.accommodation_notes.trim(),
    pay_basis: form.pay_basis,
    pay_amount: form.pay_amount.trim() ? whole(form.pay_amount) : null,
    pay_negotiable: form.pay_negotiable,
    bio: form.bio.trim(),
  };
}
