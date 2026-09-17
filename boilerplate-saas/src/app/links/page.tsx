'use client';

export default function LinksPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-50 to-white dark:from-gray-900 dark:to-gray-800">
      <main className="mx-auto max-w-4xl px-6 py-12">
        <section className="mb-12 text-center">
          <span className="inline-block rounded-full bg-purple-100 px-4 py-1 text-sm font-semibold text-purple-800">SaaS Links</span>
          <h1 className="mt-6 text-4xl font-bold text-gray-900 dark:text-white">
            LinkTree alternatif, mais mieux
          </h1>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
            Une page de liens. Tracking intégré. Analytics. Custom domain.
          </p>
        </section>

        {/* Pain */}
        <section className="mb-12 rounded-lg bg-white p-8 shadow dark:bg-gray-800">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Pourquoi pas LinkTree ?</h2>
          <ul className="mt-4 space-y-3 text-gray-600 dark:text-gray-400">
            <li>🔒 <strong>Vendor lock :</strong> Tes données leur appartiennent</li>
            <li>💰 <strong>10€/mois :</strong> Pour des liens, c'est cher</li>
            <li>📊 <strong>Pas de stats :</strong> Qui clique ? Quand ?</li>
            <li>🎨 <strong>Personnalisation limitée :</strong> Template rigide</li>
          </ul>
        </section>

        {/* Solution */}
        <section className="mb-12">
          <h2 className="mb-6 text-center text-2xl font-bold text-gray-900 dark:text-white">Ce qu'on fait</h2>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="rounded-lg border border-gray-200 p-6 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white">🔗 Liens illimités</h3>
              <p className="mt-2 text-sm text-gray-600">Drag & drop, icônes, liens masqués, analytics</p>
            </div>
            <div className="rounded-lg border border-gray-200 p-6 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white">📊 Analytics</h3>
              <p className="mt-2 text-sm text-gray-600">Clics, pays, devices, UTM tracking</p>
            </div>
            <div className="rounded-lg border border-gray-200 p-6 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white">🌐 Custom domain</h3>
              <p className="mt-2 text-sm text-gray-600">liens.tondomaine.com</p>
            </div>
            <div className="rounded-lg border border-gray-200 p-6 dark:border-gray-700">
              <h3 className="font-bold text-gray-900 dark:text-white">⚡ Ultra rapide</h3>
              <p className="mt-2 text-sm text-gray-600">Edge-deployed, 50ms worldwide</p>
            </div>
          </div>
        </section>

        {/* Pricing */}
        <section className="mb-12">
          <h2 className="mb-6 text-center text-2xl font-bold text-gray-900 dark:text-white">Tarifs</h2>
          <div className="grid gap-8 md:grid-cols-2">
            <div className="rounded-lg border border-gray-200 bg-white p-8 shadow dark:border-gray-700 dark:bg-gray-800">
              <h4 className="text-xl font-bold text-gray-900 dark:text-white">Hobby</h4>
              <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">0€<span className="text-lg font-normal text-gray-500">/mois</span></p>
              <ul className="mt-6 space-y-3 text-sm text-gray-600 dark:text-gray-400">
                <li>✅ 10 liens</li>
                <li>✅ Stats basiques</li>
                <li>❌ Custom domain</li>
              </ul>
            </div>
            <div className="rounded-lg border-2 border-purple-500 bg-white p-8 shadow-lg dark:bg-gray-800">
              <h4 className="text-xl font-bold text-gray-900 dark:text-white">Pro</h4>
              <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">9€<span className="text-lg font-normal text-gray-500">/mois</span></p>
              <ul className="mt-6 space-y-3 text-sm text-gray-600 dark:text-gray-400">
                <li>✅ Liens illimités</li>
                <li>✅ Analytics complets</li>
                <li>✅ Custom domain</li>
                <li>✅ UTM tracking</li>
              </ul>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
