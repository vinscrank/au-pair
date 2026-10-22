export type Choice = { value: string; label: string };

export type AreaGroup = { group: string; options: Choice[] };

export type Meta = {
  areas: AreaGroup[];
  duties: Choice[];
  age_bands: Choice[];
  care_windows: Choice[];
  days: Choice[];
  minds_in: Choice[];
  arrangements: Choice[];
  start_timings: Choice[];
  pay_basis: Choice[];
  genders: Choice[];
  levels: Choice[];
  languages: Choice[];
  households: Choice[];
};

export type Contact = {
  channel: 'whatsapp';
  available: boolean;
  value: string | null;
};

export type CardSection = {
  title: string;
  rows: { label: string; value: string }[];
};

export type Card = {
  user_id: string;
  role: 'candidate' | 'family';
  display_name: string;
  photo_url: string;
  kicker: string;
  headline: string;
  highlights: string[];
  bio: string;
  sections: CardSection[];
};

export type Match = {
  id: string;
  created_at: string | null;
  card: Card;
  contact: Contact;
};

export type Me = {
  id: string;
  email: string;
  role: 'candidate' | 'family';
  profile_complete: boolean;
};

export type Missing = { key: string; label: string };

export type LanguageRow = { language: string; level: string };

export type ChildRow = { age_years: string; age_months: string };

export type CandidateProfile = {
  display_name: string;
  whatsapp: string;
  photo_url: string;
  age: number | null;
  gender: string;
  nationality: string;
  based_in: string;
  languages: { language: string; level: string }[];
  experience_years: number | null;
  experience_age_bands: string[];
  experience_summary: string;
  qualification: string;
  first_aid: boolean;
  garda_vetting: boolean;
  has_references: boolean;
  smoker: boolean | null;
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
  hours_per_week: number | null;
  schedule_notes: string;
  available_short_notice: boolean;
  start_timing: string;
  duration_months: number | null;
  pay_basis: string;
  pay_min: number | null;
  pay_max: number | null;
  pay_negotiable: boolean;
  bio: string;
};

export type FamilyProfile = {
  display_name: string;
  whatsapp: string;
  photo_url: string;
  area: string;
  children: { age_years: number | null; age_months: number | null }[];
  schedule_notes: string;
  days_needed: string[];
  hours_per_week: number | null;
  care_windows: string[];
  start_timing: string;
  duration_months: number | null;
  arrangement: string;
  duties: string[];
  languages_at_home: { language: string; level: string }[];
  household: string;
  has_pets: boolean;
  pet_notes: string;
  own_room: boolean;
  accommodation_notes: string;
  pay_basis: string;
  pay_amount: number | null;
  pay_negotiable: boolean;
  bio: string;
};

export type ProfileResponse = {
  role: 'candidate' | 'family';
  complete: boolean;
  missing: Missing[];
  profile: CandidateProfile | FamilyProfile;
  card: Card;
};

export type SwipeResponse = {
  direction: 'like' | 'pass';
  matched: boolean;
  match: Match | null;
};
