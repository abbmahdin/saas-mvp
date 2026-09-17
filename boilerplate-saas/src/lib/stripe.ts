import Stripe from 'stripe';

let stripeInstance: Stripe | null = null;

export function createStripeClient(): Stripe {
  if (!stripeInstance) {
    const apiKey = process.env.STRIPE_SECRET_KEY;

    if (!apiKey) {
      throw new Error('Missing STRIPE_SECRET_KEY environment variable');
    }

    stripeInstance = new Stripe(apiKey, {
      apiVersion: '2024-06-20',
      typescript: true,
    });
  }

  return stripeInstance;
}

export async function createCustomer(email: string, name?: string): Promise<Stripe.Customer> {
  const stripe = createStripeClient();
  return stripe.customers.create({ email, name });
}

export async function createSubscription(
  customerId: string,
  priceId: string
): Promise<Stripe.Subscription> {
  const stripe = createStripeClient();
  return stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: priceId }],
    payment_behavior: 'default_incomplete',
    expand: ['latest_invoice.payment_intent'],
  });
}