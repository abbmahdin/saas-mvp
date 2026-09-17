import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { createStripeClient } from '@/lib/stripe';

const billingSchema = z.object({
  customerId: z.string().min(1),
  amount: z.number().positive(),
  currency: z.string().default('usd'),
  description: z.string().optional(),
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { customerId, amount, currency, description } = billingSchema.parse(body);

    const stripe = createStripeClient();

    const paymentIntent = await stripe.paymentIntents.create({
      amount,
      currency,
      customer: customerId,
      description,
      automatic_payment_methods: { enabled: true },
    });

    return NextResponse.json({
      clientSecret: paymentIntent.client_secret,
      paymentIntentId: paymentIntent.id,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid input', details: error.errors },
        { status: 400 }
      );
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const customerId = searchParams.get('customerId');

  if (!customerId) {
    return NextResponse.json(
      { error: 'customerId is required' },
      { status: 400 }
    );
  }

  try {
    const stripe = createStripeClient();
    const charges = await stripe.charges.list({
      customer: customerId,
      limit: 10,
    });

    return NextResponse.json({ data: charges.data });
  } catch {
    return NextResponse.json(
      { error: 'Failed to fetch billing history' },
      { status: 500 }
    );
  }
}