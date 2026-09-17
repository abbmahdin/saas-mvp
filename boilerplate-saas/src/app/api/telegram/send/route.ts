/**
 * API Route Next.js — Proxy Telegram Notifie
 * POST /api/telegram/send
 * Body: { text, parse_mode?, disable_notification? }
 */

import { NextResponse } from 'next/server';

const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const CHAT_ID = process.env.TELEGRAM_CHAT_ID;

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { text, parse_mode = 'HTML', disable_notification = false } = body;

    if (!text) {
      return NextResponse.json({ error: 'text requis' }, { status: 400 });
    }

    if (!BOT_TOKEN || !CHAT_ID) {
      return NextResponse.json({ error: 'Config Telegram manquante' }, { status: 500 });
    }

    const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: CHAT_ID,
        text,
        parse_mode,
        disable_notification,
      }),
    });

    const data = await res.json();
    return NextResponse.json({ ok: data.ok, result: data.result }, { status: data.ok ? 200 : 400 });
  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: 500 });
  }
}
