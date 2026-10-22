export function BrandMark() {
  return (
    <svg className="mark" viewBox="0 0 64 64" aria-hidden="true">
      <rect width="64" height="64" rx="18" fill="#1C2B26" />
      <path
        d="M14 42V30L32 16l18 14v12"
        fill="none"
        stroke="#F3EEE6"
        strokeWidth="4"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
      <circle cx="32" cy="36" r="4.5" fill="#C6533A" />
    </svg>
  );
}

export function Wordmark({ compact = false }: { compact?: boolean }) {
  return (
    <span className={compact ? 'wordmark compact' : 'wordmark'}>
      <BrandMark />
      <span>Mobijob</span>
    </span>
  );
}
