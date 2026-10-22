import Link from 'next/link';
import { Wordmark } from '@/components/BrandMark';

export default function WelcomePage() {
  return (
    <main className="split">
      <section className="split-story">
        <Wordmark />
        <h1 className="display">Find care. Find a family.</h1>
        <p className="lede">Au pair matches au pairs and babysitters with host families in Dublin.</p>
        <ul className="points">
          <li>
            <strong>Practical profiles.</strong> Areas, hours, children and pay are on the card.
          </li>
          <li>
            <strong>Both sides choose.</strong> A family can send interest. You can apply.
          </li>
          <li>
            <strong>WhatsApp when it is mutual.</strong> The number stays closed until you both say yes.
          </li>
        </ul>
        <p className="quiet">Dublin first.</p>
      </section>
      <section className="split-panel">
        <div className="panel-card">
          <h2 className="display">Start with a profile, not a group chat.</h2>
          <p>Host families and people who mind children. Any gender. No payment to join.</p>
          <div className="stack">
            <Link className="btn btn-clay" href="/signup">
              Create an account
            </Link>
            <Link className="btn btn-ghost" href="/login">
              I already have an account
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
