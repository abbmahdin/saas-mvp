'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface Signal {
  id: string;
  direction: 'BUY' | 'SELL';
  entry: number;
  stop_loss: number;
  take_profit: number;
  confidence: number;
  timeframe: string;
  timestamp: string;
  status: 'active' | 'closed' | 'target_hit';
}

// Signaux de démonstration (mock data)
const MOCK_SIGNALS: Signal[] = [
  {
    id: 'sig_1',
    direction: 'BUY',
    entry: 2342.5,
    stop_loss: 2335.2,
    take_profit: 2358.0,
    confidence: 92.3,
    timeframe: 'H1',
    timestamp: new Date().toISOString(),
    status: 'active',
  },
  {
    id: 'sig_2',
    direction: 'SELL',
    entry: 2355.0,
    stop_loss: 2362.5,
    take_profit: 2342.0,
    confidence: 88.7,
    timeframe: 'H1',
    timestamp: new Date(Date.now() - 3600000).toISOString(),
    status: 'target_hit',
  },
  {
    id: 'sig_3',
    direction: 'BUY',
    entry: 2338.0,
    stop_loss: 2330.0,
    take_profit: 2350.0,
    confidence: 87.5,
    timeframe: 'H4',
    timestamp: new Date(Date.now() - 14400000).toISOString(),
    status: 'closed',
  },
];

export default function Dashboard() {
  const [email, setEmail] = useState<string | null>(null);
  const [signals, setSignals] = useState<Signal[]>(MOCK_SIGNALS);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Récupérer l'email depuis la session Supabase
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (user) {
        setEmail(user.email ?? null);
      }
      setLoading(false);
    };
    getUser();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-yellow-400 mx-auto mb-4"></div>
          <p className="text-gray-400">Chargement du dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Header */}
      <header className="bg-gray-900/50 border-b border-gray-800 px-6 py-4">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-yellow-400">
            GoldSignals
          </Link>
          <div className="flex items-center gap-4">
            {email ? (
              <span className="text-sm text-gray-400">{email}</span>
            ) : (
              <Link
                href="/"
                className="text-sm text-gray-400 hover:text-yellow-400 transition-colors"
              >
                Connecter
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-6">Signaux XAU/USD</h1>

        {/* Signals Table */}
        <div className="bg-gray-900/30 rounded-xl border border-gray-800 overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-800/50">
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Signal</th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Direction</th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Entry</th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">SL</th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">TP</th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Confiance</th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Status</th>
                <th className="text-left px-4 py-3 text-sm font-medium text-gray-300">Timeframe</th>
              </tr>
            </thead>
            <tbody>
              {signals.map((signal) => (
                <tr key={signal.id} className="border-t border-gray-800">
                  <td className="px-4 py-3 text-sm font-mono text-gray-400">#{signal.id}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`font-bold ${
                        signal.direction === 'BUY'
                          ? 'text-green-400'
                          : 'text-red-400'
                      }`}
                    >
                      {signal.direction}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm">{signal.entry.toFixed(1)}</td>
                  <td className="px-4 py-3 text-sm text-red-400">{signal.stop_loss.toFixed(1)}</td>
                  <td className="px-4 py-3 text-sm text-green-400">{signal.take_profit.toFixed(1)}</td>
                  <td className="px-4 py-3">
                    <span className="text-sm text-yellow-400">{signal.confidence.toFixed(1)}%</span>
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${
                        signal.status === 'active'
                          ? 'bg-green-500/20 text-green-400'
                          : signal.status === 'target_hit'
                          ? 'bg-blue-500/20 text-blue-400'
                          : 'bg-gray-500/20 text-gray-400'
                      }`}
                    >
                      {signal.status === 'active'
                        ? 'Actif'
                        : signal.status === 'target_hit'
                        ? 'Take Profit'
                        : 'Fermé'}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-sm text-gray-400">{signal.timeframe}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Legend */}
        <div className="mt-6 bg-gray-900/30 rounded-xl border border-gray-800 p-4">
          <h2 className="font-semibold mb-2 text-sm text-gray-300">Légende</h2>
          <ul className="text-sm text-gray-400 space-y-1">
            <li>• <span className="text-green-400 font-bold">BUY</span> = Position Long</li>
            <li>• <span className="text-red-400 font-bold">SELL</span> = Position Short</li>
            <li>• <span className="text-green-400">Actif</span> = Signal en cours</li>
            <li>• <span className="text-blue-400">Take Profit</span> = Objectif atteint</li>
            <li>• <span className="text-gray-400">Fermé</span> = Signal clôturé</li>
            <li>• <span className="text-yellow-400">Confiance</span> = Score de conviction SMC/CVD</li>
          </ul>
        </div>

        {/* Upgrade prompt */}
        <div className="mt-6 text-center">
          <Link
            href="/subscribe"
            className="inline-block px-6 py-3 bg-yellow-400 text-black font-bold rounded-lg hover:bg-yellow-300 transition"
          >
            Passer à GoldSignals Pro 49€/mois
          </Link>
        </div>
      </main>
    </div>
  );
}
