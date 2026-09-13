import './globals.css';

export const metadata = {
  title: 'Boilerplate SaaS',
  description: 'Modern SaaS boilerplate with Next.js, Supabase, Stripe, and AI capabilities',
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