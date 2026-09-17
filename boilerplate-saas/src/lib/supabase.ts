import { createClient } from '@supabase/supabase-js';

// IMPORTANT: Replace the anon key in .env.local with the FULL key from Supabase dashboard
// The current one in .env.local is truncated (eyJhbG...Z6iM)
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

if (!supabaseUrl || !supabaseKey) {
  throw new Error('Supabase URL and key must be set in .env.local');
}

export const supabase = createClient(supabaseUrl, supabaseKey);

// Subscribe user to free plan
export async function subscribe(email: string, plan: string = 'free') {
  try {
    const { data, error } = await supabase
      .from('subscribers')
      .insert({
        email,
        plan,
        status: 'active',
        created_at: new Date().toISOString(),
      })
      .select();

    return { success: !error, data, error };
  } catch (err) {
    return { success: false, error: err };
  }
}
