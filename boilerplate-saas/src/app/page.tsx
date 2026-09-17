'use client';

import { useState } from 'react';

interface Signal {
  id: string;
  direction: 'BUY' | 'SELL';
  price: number;
  stop_loss: number;
  take_profit: number;
  confidence: number;
  reason: string;
  created_at: string;
}

const mockSignals: Signal[] = [
  { id: '1', direction: 'BUY', price: 2456.50, stop_loss: 2446.50, take_profit: 2476.50, confidence: 85, reason: 'SMC Order Block + CVD Divergence', created_at: '2026-09-17T10:30:00Z' },
  { id: '2', direction: 'SELL', price: 2478.20, stop_loss: 2488.20, take_profit: 2458.20, confidence: 78, reason: 'Liquidity Sweep + FVG Fill', created_at: '2026-09-17T08:15:00Z' },
  { id: '3', direction: 'BUY', price: 2432.10, stop_loss: 2422.10, take_profit: 2452.10, confidence: 92, reason: 'Daily OB + 4H FVG + CVD Confirmation', created_at: '2026-09-16T14:45:00Z' },
];

function SignalCard({ signal }: { signal: Signal }) {
  const isBuy = signal.direction === 'BUY';
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <span className={`rounded-full px-3 py-1 text-sm font-bold ${isBuy ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>{signal.direction}</span>
        <span className="text-sm text-gray-500">{new Date(signal.created_at).toLocaleString('fr-FR')}</span>
      </div>
      <div className="mt-3 grid grid-cols-3 gap-4 text-center">
        <div><p className="text-xs text-gray-500">Entrée</p><p className="font-mono font-bold">${signal.price.toFixed(2)}</p></div>
        <div><p className="text-xs text-gray-500">SL</p><p className="font-mono text-red-600">${signal.stop_loss.toFixed(2)}</p></div>
        <div><p className="text-xs text-gray-500">TP</p><p className="font-mono text-green-600">${signal.take_profit.toFixed(2)}</p></div>
      </div>
      <p className="mt-3 text-sm text-gray-600">{signal.reason}</p>
    </div>
  );
}

export default function LandingPage() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFree = async () => {
    if (!email || !email.includes('@')) {
      setMessage('Veuillez entrer un email valide');
      return;
    }
    setLoading(true);
    setMessage('');
    try {
      const res = await fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, plan: 'free' }),
      });
      const data = await res.json();
      if (data.success) {
        setMessage('✅ Inscrit avec succès ! Vérifiez votre email.');
        setEmail('');
      } else {
        setMessage('❌ Erreur: ' + (data.error || 'inconnue'));
      }
    } catch (err) {
      setMessage('❌ Erreur réseau');
    }
    setLoading(false);
  };

  const handlePro = async () => {
    if (!email || !email.includes('@')) {
      setMessage('Veuillez entrer un email valide');
      return;
    }
    setLoading(true);
    setMessage('');
    try {
      const res = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, plan: 'pro' }),
      });
      const data = await res.json();
      if (data.url) {
        window.location.href = data.url;
      } else {
        setMessage('❌ Erreur: ' + (data.error || 'inconnue'));
      }
    } catch (err) {
      setMessage('❌ Erreur réseau');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <header className="border-b border-gray-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <h1 className="text-xl font-bold text-gray-900">GoldSignals</h1>
          <nav className="flex gap-6">
            <a href="#signals" className="text-sm text-gray-600 hover:text-gray-900">Signaux</a>
            <a href="#pricing" className="text-sm text-gray-600 hover:text-gray-900">Tarifs</a>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-12">
        <section className="mb-16 text-center">
          <h2 className="text-4xl font-bold text-gray-900">Signaux XAUUSD <span className="text-yellow-500">SMC/CVD</span></h2>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-600">Backtestés, automatisés, livrés en temps réel sur Telegram.</p>
        </section>

        <section className="mb-16 grid grid-cols-3 gap-8 text-center">
          <div className="rounded-lg bg-white p-6 shadow"><p className="text-3xl font-bold text-yellow-500">73%</p><p className="mt-2 text-sm text-gray-600">Win Rate</p></div>
          <div className="rounded-lg bg-white p-6 shadow"><p className="text-3xl font-bold text-yellow-500">1:2.5</p><p className="mt-2 text-sm text-gray-600">R:R moyen</p></div>
          <div className="rounded-lg bg-white p-6 shadow"><p className="text-3xl font-bold text-yellow-500">150+</p><p className="mt-2 text-sm text-gray-600">Signaux/mois</p></div>
        </section>

        <section id="signals" className="mb-16">
          <h3 className="mb-6 text-2xl font-bold">Derniers signaux</h3>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {mockSignals.map((s) => <SignalCard key={s.id} signal={s} />)}
          </div>
        </section>

        {/* CTA Principal */}
        <section id="pricing" className="mb-16 max-w-md mx-auto">
          <h3 className="mb-6 text-center text-2xl font-bold">Commencer</h3>
          <div className="rounded-lg border-2 border-yellow-500 bg-white p-8 shadow-lg">
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700">Votre email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="votre@email.com"
                className="mt-1 w-full rounded-lg border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-yellow-500"
              />
            </div>
            <button
              onClick={handleFree}
              disabled={loading}
              className="w-full rounded-lg border-2 border-yellow-500 py-3 font-semibold text-yellow-600 hover:bg-yellow-50 disabled:opacity-50"
            >
              {loading ? '...' : 'Commencer gratuitement'}
            </button>
            <button
              onClick={handlePro}
              disabled={loading}
              className="mt-3 w-full rounded-lg bg-yellow-500 py-3 font-semibold text-white hover:bg-yellow-600 disabled:opacity-50"
            >
              {loading ? '...' : "S'abonner Pro — 49€/mois"}
            </button>
            {message && <p className="mt-4 text-center text-sm">{message}</p>}
          </div>
          <p className="mt-4 text-center text-xs text-gray-500">Essai gratuit • Annulez à tout moment • Sans engagement</p>
        </section>

        {/* FAQ */}
        <section className="mb-16">
          <h3 className="mb-6 text-2xl font-bold">FAQ</h3>
          <div className="space-y-4">
            <details className="rounded-lg border border-gray-200 bg-white p-4">
              <summary className="cursor-pointer font-semibold">Qu'est-ce que SMC/CVD ?</summary>
              <p className="mt-2 text-sm text-gray-600">Smart Money Concepts (SMC) est une méthodologie de trading institutionnelle. CVD mesure l'achat/vente agressif.</p>
            </details>
            <details className="rounded-lg border border-gray-200 bg-white p-4">
              <summary className="cursor-pointer font-semibold">Puis-je annuler à tout moment ?</summary>
              <p className="mt-2 text-sm text-gray-600">Oui. Pas de engagement. Annulez en 1 clic.</p>
            </details>
          </div>
        </section>
      </main>

      <footer className="border-t border-gray-200 bg-white py-8">
        <div className="mx-auto max-w-6xl px-6 text-center text-sm text-gray-500">
          <p>© 2026 GoldSignals. Le trading comporte des risques.</p>
        </div>
      </footer>
    </div>
  );
}
