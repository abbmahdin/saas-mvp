'use client';

export default function InvoicePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-800">
      <main className="mx-auto max-w-4xl px-6 py-12">
        <section className="mb-12 text-center">
          <span className="inline-block rounded-full bg-blue-100 px-4 py-1 text-sm font-semibold text-blue-800">SaaS Invoice</span>
          <h1 className="mt-6 text-4xl font-bold text-gray-900 dark:text-white">
            Factures automatiques pour freelances & PME
          </h1>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
            Créez, envoyez et suivez vos factures en 2 minutes. Intégré Stripe + Supabase.
          </p>
        </section>

        {/* Pain */}
        <section className="mb-12 rounded-lg bg-white p-8 shadow dark:bg-gray-800">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Le problème</h2>
          <ul className="mt-4 space-y-3 text-gray-600 dark:text-gray-400">
            <li>⏰ <strong>Temps perdu :</strong> 4h/semaine à créer des factures manuellement</li>
            <li>📧 <strong>Relances :</strong> Difficile de suivre les impayés</li>
            <li>📊 <strong>Comptabilité :</strong> Pas de synchronisation avec le comptable</li>
            <li>💳 <strong>Paiements :</strong> Processus complexes pour les clients</li>
          </ul>
        </section>

        {/* Solution */}
        <section className="mb-12">
          <h2 className="mb-6 text-center text-2xl font-bold text-gray-900 dark:text-white">La solution</h2>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="rounded-lg border border-gray-200 p-6 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white">📝 Création rapide</h3>
              <p className="mt-2 text-sm text-gray-600">Template pro, sauvegarde client, envoi automatique</p>
            </div>
            <div className="rounded-lg border border-gray-200 p-6 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white">💳 Paiement intégré</h3>
              <p className="mt-2 text-sm text-gray-600">Stripe Checkout, lien de paiement par email</p>
            </div>
            <div className="rounded-lg border border-gray-200 p-6 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white">📊 Dashboard</h3>
              <p className="mt-2 text-sm text-gray-600">Revenus, impayés, prévisions mensuelles</p>
            </div>
            <div className="rounded-lg border border-gray-200 p-6 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white">📤 Export comptable</h3>
              <p className="mt-2 text-sm text-gray-600">CSV, PDF, synchronisation automatique</p>
            </div>
          </div>
        </section>

        {/* Pricing */}
        <section className="mb-12">
          <h2 className="mb-6 text-center text-2xl font-bold text-gray-900 dark:text-white">Tarifs</h2>
          <div className="grid gap-8 md:grid-cols-2">
            <div className="rounded-lg border border-gray-200 bg-white p-8 shadow dark:border-gray-700 dark:bg-gray-800">
              <h4 className="text-xl font-bold text-gray-900 dark:text-white">Starter</h4>
              <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">0€<span className="text-lg font-normal text-gray-500">/mois</span></p>
              <ul className="mt-6 space-y-3 text-sm text-gray-600 dark:text-gray-400">
                <li>✅ 5 factures/mois</li>
                <li>✅ 1 client</li>
                <li>✅ Paiement Stripe</li>
                <li>❌ Multi-devises</li>
              </ul>
            </div>
            <div className="rounded-lg border-2 border-blue-500 bg-white p-8 shadow-lg dark:bg-gray-800">
              <h4 className="text-xl font-bold text-gray-900 dark:text-white">Pro</h4>
              <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">29€<span className="text-lg font-normal text-gray-500">/mois</span></p>
              <ul className="mt-6 space-y-3 text-sm text-gray-600 dark:text-gray-400">
                <li>✅ Factures illimitées</li>
                <li>✅ Clients illimités</li>
                <li>✅ Multi-devises</li>
                <li>✅ Export comptable</li>
              </ul>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
