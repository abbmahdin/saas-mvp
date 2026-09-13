import Dashboard from '@/components/Dashboard';
import Chat from '@/components/Chat';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col">
      <header className="border-b border-gray-200 px-6 py-4 dark:border-gray-800">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <h1 className="text-xl font-bold">SaaS Boilerplate</h1>
          <nav className="flex gap-4">
            <a href="#dashboard" className="text-sm hover:underline">Dashboard</a>
            <a href="#chat" className="text-sm hover:underline">AI Chat</a>
          </nav>
        </div>
      </header>
      <div className="flex-1 px-6 py-8">
        <div className="mx-auto max-w-7xl space-y-12">
          <Dashboard />
          <div id="chat">
            <h2 className="mb-4 text-2xl font-bold">AI Assistant</h2>
            <Chat />
          </div>
        </div>
      </div>
    </main>
  );
}