export function WizardFrame({
  step,
  count,
  title,
  lede,
  error,
  missing,
  saving,
  onBack,
  onNext,
  isLast,
  children,
}: {
  step: number;
  count: number;
  title: string;
  lede: string;
  error: string;
  missing: string[];
  saving: boolean;
  onBack: () => void;
  onNext: () => void;
  isLast: boolean;
  children: React.ReactNode;
}) {
  return (
    <div className="wizard">
      <p className="eyebrow">
        Step {step + 1} of {count}
      </p>
      <div className="progress" aria-hidden="true">
        <span style={{ width: `${((step + 1) / count) * 100}%` }} />
      </div>
      <h1 className="display">{title}</h1>
      <p className="lede">{lede}</p>
      {error ? (
        <div className="alert" role="alert">
          {error}
        </div>
      ) : null}
      {missing.length ? (
        <div className="alert" role="alert">
          Still needed: {missing.join(', ')}.
        </div>
      ) : null}
      <div className="wizard-body">{children}</div>
      <div className="wizard-footer">
        {step > 0 ? (
          <button type="button" className="btn btn-ghost" onClick={onBack} disabled={saving}>
            Back
          </button>
        ) : null}
        <button type="button" className="btn btn-clay" onClick={onNext} disabled={saving}>
          {saving ? 'Saving' : isLast ? 'Finish profile' : 'Continue'}
        </button>
      </div>
    </div>
  );
}
