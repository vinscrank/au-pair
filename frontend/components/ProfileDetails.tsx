import type { Card } from '@/lib/types';

export function ProfileDetails({ card }: { card: Card }) {
  return (
    <div className="details">
      {card.sections.map((section) => (
        <section key={section.title}>
          <h3>{section.title}</h3>
          <dl>
            {section.rows.map((row) => (
              <div key={row.label}>
                <dt>{row.label}</dt>
                <dd>{row.value}</dd>
              </div>
            ))}
          </dl>
        </section>
      ))}
    </div>
  );
}
