import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createStripeClient, createCustomer, createSubscription } from '@/lib/stripe';

vi.mock('stripe', () => {
  return {
    default: vi.fn().mockImplementation(() => ({
      paymentIntents: { create: vi.fn() },
      customers: { create: vi.fn() },
      subscriptions: { create: vi.fn() },
      charges: { list: vi.fn() },
    })),
  };
});

describe('Stripe Client', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    vi.resetModules();
    process.env = {
      ...originalEnv,
      STRIPE_SECRET_KEY: 'sk_test_123',
    };
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  it('should throw error if STRIPE_SECRET_KEY is missing', () => {
    delete process.env.STRIPE_SECRET_KEY;
    expect(() => createStripeClient()).toThrow('Missing STRIPE_SECRET_KEY environment variable');
  });

  it('should create a singleton Stripe client', () => {
    const client1 = createStripeClient();
    const client2 = createStripeClient();
    expect(client1).toBe(client2);
  });

  it('should create a customer', async () => {
    const stripe = createStripeClient();
    const mockCustomer = { id: 'cus_123', email: 'test@example.com' };
    vi.mocked(stripe.customers.create).mockResolvedValue(mockCustomer as any);

    const customer = await createCustomer('test@example.com');
    expect(customer).toEqual(mockCustomer);
  });

  it('should create a subscription', async () => {
    const stripe = createStripeClient();
    const mockSubscription = { id: 'sub_123', status: 'incomplete' };
    vi.mocked(stripe.subscriptions.create).mockResolvedValue(mockSubscription as any);

    const subscription = await createSubscription('cus_123', 'price_123');
    expect(subscription).toEqual(mockSubscription);
  });
});