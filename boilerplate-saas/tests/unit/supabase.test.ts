import { describe, it, expect, vi, beforeEach } from 'vitest';
import { resetSupabaseClient, getSupabaseClient } from '@/lib/supabase';

describe('Supabase Client', () => {
  beforeEach(() => {
    resetSupabaseClient();
    vi.clearAllMocks();
  });

  it('returns a singleton instance', () => {
    const client1 = getSupabaseClient();
    const client2 = getSupabaseClient();
    expect(client1).toBe(client2);
  });

  it('throws if env vars are missing', () => {
    vi.stubEnv('NEXT_PUBLIC_SUPABASE_URL', '');
    vi.stubEnv('NEXT_PUBLIC_SUPABASE_ANON_KEY', '');
    resetSupabaseClient();

    expect(() => getSupabaseClient()).toThrow('Missing Supabase environment variables');
  });
});
