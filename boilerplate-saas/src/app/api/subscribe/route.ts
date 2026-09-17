import { NextResponse } from 'next/server';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function POST(request: Request) {
  try {
    const { email, plan } = await request.json();
    
    if (!email || !email.includes('@')) {
      return NextResponse.json({ error: 'Email invalide' }, { status: 400 });
    }

    // 1. Stocker dans Supabase (table subscribers à créer dans le Dashboard)
    const { error } = await supabase
      .from('subscribers')
      .insert({ email, plan: plan || 'free', status: 'active' });

    if (error) {
      // Fallback: log + notification Telegram
      console.log(`Inscription: ${email} (Supabase: ${error.message})`);
    }

    // 2. Envoyer email de confirmation via Resend
    const resendKey = process.env.RESEND_API_KEY;
    if (resendKey) {
      try {
        await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${resendKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            from: 'GoldSignals <delivered@resend.dev>',
            to: [email],
            subject: 'Bienvenue sur GoldSignals — Confirmation',
            html: `<div style="font-family: system-ui, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
<h1 style="color: #eab308;">Bienvenue sur GoldSignals !</h1>
<p>Votre inscription au plan <strong>${plan || 'gratuit'}</strong> est confirmée.</p>
<ul>
<li>Vous recevrez vos premiers signaux sur Telegram</li>
<li>Accès au dashboard client prochainement</li>
<li>Support : contact@goldsignals.app</li>
</ul>
— L'équipe GoldSignals
</div>`,
          }),
        });
      } catch (e) {
        console.log('Email error:', e);
      }
    }

    // 3. Notification Telegram (optionnel)
    const botToken = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_CHAT_ID;
    if (botToken && chatId) {
      try {
        await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            chat_id: chatId,
            text: '📧 Nouvel inscrit GoldSignals\nEmail: ' + email + '\nPlan: ' + (plan || 'free'),
          }),
        });
      } catch (e) {
        console.log('Telegram error:', e);
      }
    }

    return NextResponse.json({ success: true, message: 'Inscrit ! Vérifiez votre email.' });
  } catch (error) {
    console.error('Subscribe error:', error);
    return NextResponse.json({ error: 'Erreur serveur' }, { status: 500 });
  }
}
