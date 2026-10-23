import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import QueryProvider from '@/providers/QueryProvider';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter', display: 'swap' });

export const metadata: Metadata = {
  title: 'SARA 777 Admin',
  description: 'Operations console for SARA 777: markets, results, bids, rates, wallet, and users.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
