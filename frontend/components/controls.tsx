'use client';

import { cloneElement, isValidElement, useState } from 'react';
import { ApiError, api } from '@/lib/api';
import type { AreaGroup, ChildRow, Choice, LanguageRow } from '@/lib/types';

export function Field({ label, hint, children }: { label: string; hint?: string; children: React.ReactElement<{ 'aria-label'?: string }> }) {
  const control = isValidElement(children) ? cloneElement(children, { 'aria-label': label }) : children;
  return (
    <div className="field">
      <span>{label}</span>
      {control}
      {hint ? <small>{hint}</small> : null}
    </div>
  );
}

export function ChipSet({
  options,
  value,
  onChange,
  single = false,
}: {
  options: Choice[];
  value: string[];
  onChange: (next: string[]) => void;
  single?: boolean;
}) {
  return (
    <div className="chips" role={single ? 'radiogroup' : 'group'}>
      {options.map((option) => {
        const on = value.includes(option.value);
        return (
          <button
            key={option.value}
            type="button"
            className={on ? 'chip on' : 'chip'}
            aria-pressed={on}
            onClick={() => {
              if (single) {
                onChange([option.value]);
                return;
              }
              onChange(on ? value.filter((item) => item !== option.value) : [...value, option.value]);
            }}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}

export function AreaPicker({
  groups,
  selected,
  multiple,
  onChange,
}: {
  groups: AreaGroup[];
  selected: string[];
  multiple: boolean;
  onChange: (next: string[]) => void;
}) {
  const [query, setQuery] = useState('');
  const names = groups.flatMap((group) => group.options.map((option) => option.value));
  const needle = query.trim().toLowerCase();
  const matches = (needle ? names.filter((name) => name.toLowerCase().includes(needle)) : names).slice(0, 8);

  function choose(name: string) {
    if (!multiple) {
      onChange([name]);
      setQuery('');
      return;
    }
    if (selected.includes(name) || selected.length >= 8) return;
    onChange([...selected, name]);
    setQuery('');
  }

  return (
    <div className="area-picker">
      {selected.length ? (
        <div className="chips">
          {selected.map((name) => (
            <button
              key={name}
              type="button"
              className="chip on"
              onClick={() => onChange(selected.filter((item) => item !== name))}
            >
              {name}
            </button>
          ))}
        </div>
      ) : null}
      <input
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="Search Dublin areas"
        aria-label="Search Dublin areas"
      />
      <div className="suggest">
        {matches.map((name) => (
          <button key={name} type="button" className="suggest-item" onClick={() => choose(name)}>
            {name}
          </button>
        ))}
      </div>
    </div>
  );
}

export function Check({ label, hint, checked, onChange }: { label: string; hint?: string; checked: boolean; onChange: (next: boolean) => void }) {
  return (
    <button type="button" className={checked ? 'check on' : 'check'} aria-pressed={checked} onClick={() => onChange(!checked)}>
      <span>
        {label}
        {hint ? <small>{hint}</small> : null}
      </span>
      <strong>{checked ? 'Yes' : 'No'}</strong>
    </button>
  );
}

export function LanguageEditor({
  rows,
  languages,
  levels,
  onChange,
}: {
  rows: LanguageRow[];
  languages: Choice[];
  levels: Choice[];
  onChange: (next: LanguageRow[]) => void;
}) {
  function update(index: number, partial: Partial<LanguageRow>) {
    onChange(rows.map((row, rowIndex) => (rowIndex === index ? { ...row, ...partial } : row)));
  }

  return (
    <div className="stack">
      {rows.map((row, index) => (
        <div className="pair" key={`${index}-${row.language}`}>
          <select aria-label="Language" value={row.language} onChange={(event) => update(index, { language: event.target.value })}>
            <option value="">Language</option>
            {languages.map((choice) => (
              <option key={choice.value} value={choice.value}>
                {choice.label}
              </option>
            ))}
          </select>
          <select aria-label="Level" value={row.level} onChange={(event) => update(index, { level: event.target.value })}>
            <option value="">Level</option>
            {levels.map((choice) => (
              <option key={choice.value} value={choice.value}>
                {choice.label}
              </option>
            ))}
          </select>
          {rows.length > 1 ? (
            <button type="button" className="text-btn" onClick={() => onChange(rows.filter((_, rowIndex) => rowIndex !== index))}>
              Remove
            </button>
          ) : null}
        </div>
      ))}
      <button type="button" className="text-btn" onClick={() => onChange([...rows, { language: '', level: '' }])}>
        Add a language
      </button>
    </div>
  );
}

export function ChildEditor({ rows, onChange }: { rows: ChildRow[]; onChange: (next: ChildRow[]) => void }) {
  function update(index: number, partial: Partial<ChildRow>) {
    onChange(rows.map((row, rowIndex) => (rowIndex === index ? { ...row, ...partial } : row)));
  }

  return (
    <div className="stack">
      {rows.map((row, index) => (
        <div className="pair" key={`child-${index}`}>
          <input
            inputMode="numeric"
            aria-label={`Child ${index + 1} age in years`}
            placeholder="Years"
            value={row.age_years}
            onChange={(event) => update(index, { age_years: event.target.value.replace(/\D/g, '').slice(0, 2) })}
          />
          <input
            inputMode="numeric"
            aria-label={`Child ${index + 1} extra months`}
            placeholder="Months, optional"
            value={row.age_months}
            onChange={(event) => update(index, { age_months: event.target.value.replace(/\D/g, '').slice(0, 2) })}
          />
          {rows.length > 1 ? (
            <button type="button" className="text-btn" onClick={() => onChange(rows.filter((_, rowIndex) => rowIndex !== index))}>
              Remove
            </button>
          ) : null}
        </div>
      ))}
      <button type="button" className="text-btn" onClick={() => onChange([...rows, { age_years: '', age_months: '' }])}>
        Add a child
      </button>
    </div>
  );
}

export function PhotoField({ url, onUploaded }: { url: string; onUploaded: (url: string) => void }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function onFile(file: File | undefined) {
    if (!file) return;
    setBusy(true);
    setError('');
    try {
      const body = new FormData();
      body.append('file', file);
      const result = await api<{ photo_url: string }>('/profile/photo', { method: 'POST', body });
      onUploaded(result.photo_url);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not upload that photo.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="photo-field">
      <div className="photo-frame">{url ? <img src={url} alt="Profile" /> : <span>A clear photo. For families, the house is fine.</span>}</div>
      <label className="btn btn-ghost file-btn">
        {busy ? 'Uploading' : url ? 'Change photo' : 'Upload photo'}
        <input
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={(event) => {
            const file = event.target.files?.[0];
            event.target.value = '';
            void onFile(file);
          }}
        />
      </label>
      {error ? <small className="danger">{error}</small> : <small>JPG, PNG or WebP, up to 5MB.</small>}
    </div>
  );
}
