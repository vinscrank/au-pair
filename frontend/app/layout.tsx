import type { Metadata } from 'next';
import { Fraunces, Outfit } from 'next/font/google';
import { Providers } from '@/app/providers';
import './globals.css';

const display = Fraunces({ subsets: ['latin'], variable: '--font-display' });
const sans = Outfit({ subsets: ['latin'], variable: '--font-body' });

export const metadata: Metadata = {
  title: 'Mobijob',
  description: 'Mobijob matches au pairs and babysitters with host families in Dublin.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${display.variable} ${sans.variable}`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
