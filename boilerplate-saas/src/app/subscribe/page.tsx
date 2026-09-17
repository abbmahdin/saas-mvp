'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabase';

export default function SubscribePage() {
  const [email, setEmail] = useState('');
  const [plan, setPlan] = useState<'free' | 'pro'>('free');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');

    if (plan === 'pro') {
      // Rediriger vers Stripe Checkout
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
          setStatus('error');
          setMessage(data.error || 'Erreur');
        }
      } catch (err) {
        setStatus('error');
        setMessage('Erreur de connexion');
      }
    } else {
      // Plan gratuit → subscribe API
      try {
        const res = await fetch('/api/subscribe', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, plan: 'free' }),
        });
        const data = await res.json();
        if (data.success) {
          setStatus('success');
          setMessage('✅ Inscription réussie ! Vérifiez votre email.');
          // Stocker l'email en session
          localStorage.setItem('user_email', email);
        } else {
          setStatus('error');
          setMessage(data.error || 'Erreur');
        }
      } catch (err) {
        setStatus('error');
        setMessage('Erreur de connexion');
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 flex items-center justify-center">
      <div className="max-w-md w-full mx-4">
        <div className="bg-gray-900 rounded-xl border border-gray-800 p-8">
          <h1 className="text-2xl font-bold text-center mb-6 text-yellow-400">
            Choisissez votre plan
          </h1>

          <div className="flex gap-3 mb-6">
            <button
              type="button"
              onClick={() => setPlan('free')}
              className={`flex-1 py-3 px-4 rounded-lg font-medium transition ${
                plan === 'free'
                  ? 'bg-yellow-400 text-black'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              Gratuit
            </button>
            <button
              type="button"
              onClick={() => setPlan('pro')}
              className={`flex-1 py-3 px-4 rounded-lg font-medium transition ${
                plan === 'pro'
                  ? 'bg-yellow-400 text-black'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              Pro — 49€/mois
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Email</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 rounded-lg border border-gray-700 focus:border-yellow-400 focus:outline-none"
                placeholder="vous@exemple.com"
                disabled={status === 'loading'}
              />
            </div>

            <button
              type="submit"
              disabled={status === 'loading'}
              className="w-full py-3 bg-yellow-400 text-black font-bold rounded-lg hover:bg-yellow-300 transition flex items-center justify-center gap-2"
            >
              {status === 'loading' ? '...' : plan === 'free' ? 'Commencer gratuitement' : "S'abonner Pro"}
            </button>

            {status === 'success' && (
              <p className="text-center text-green-400 text-sm">{message}</p>
            )}
            {status === 'error' && (
              <p className="text-center text-red-400 text-sm">{message}</p>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}
