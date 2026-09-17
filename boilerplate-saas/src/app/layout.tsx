import './globals.css';

export const metadata = {
  title: 'GoldSignals — Signaux XAUUSD SMC/CVD',
  description: 'Signaux de trading XAUUSD basés sur Smart Money Concepts et CVD. Backtestés et livrés en temps réel.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-white text-gray-900 antialiased dark:bg-gray-950 dark:text-gray-100">
        {children}
      </body>
    </html>
  );
}