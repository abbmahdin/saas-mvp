import { NextResponse } from 'next/server';

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

export async function POST(request: Request) {
  try {
    const { email, plan } = await request.json();

    if (!email || !plan) {
      return NextResponse.json({ error: 'Email et plan requis' }, { status: 400 });
    }

    const plans = {
      pro: { name: 'GoldSignals Pro', amount: 4900, interval: 'month', currency: 'eur' },
    };

    const selectedPlan = plans[plan as keyof typeof plans] || plans.pro;

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price_data: {
            currency: selectedPlan.currency,
            product_data: { name: selectedPlan.name, description: 'Signaux XAUUSD SMC/CVD en temps réel' },
            unit_amount: selectedPlan.amount,
            recurring: { interval: selectedPlan.interval as 'month' },
          },
          quantity: 1,
        },
      ],
      mode: 'subscription',
      success_url: `${process.env.NEXT_PUBLIC_SUPABASE_URL?.replace('.co', '.co/dashboard')}?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.NEXT_PUBLIC_SUPABASE_URL?.replace('.co', '.co')}`,
      customer_email: email,
      metadata: { plan, source: 'landing_page' },
    });

    return NextResponse.json({ url: session.url });
  } catch (error: any) {
    console.error('Stripe error:', error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
