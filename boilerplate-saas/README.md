# Boilerplate SaaS

Modern SaaS boilerplate built with Next.js 14, Supabase, Stripe, Tailwind CSS, and TypeScript. Includes authentication, billing, dashboard, AI chat/completion components, and a TDD workflow with Vitest.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Database/Auth**: Supabase
- **Payments**: Stripe
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Testing**: Vitest + Testing Library
- **CI/CD**: GitHub Actions

## Features

- 🔐 **Authentication** - Supabase Auth with email/password
- 💳 **Billing** - Stripe payment intents and subscriptions
- 📊 **Dashboard** - Stats cards with key metrics
- 🤖 **AI Chat** - OpenAI chat integration with streaming support
- ✅ **TDD** - Full test coverage with Vitest
- 🚀 **CI/CD** - GitHub Actions pipeline

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Supabase account
- Stripe account
- OpenAI API key (for AI features)

### Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd boilerplate-saas
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   ```

4. Configure your `.env.local`:
   ```
   NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
   STRIPE_SECRET_KEY=your-stripe-secret-key
   OPENAI_API_KEY=your-openai-api-key
   ```

5. Run the development server:
   ```bash
   npm run dev
   ```

6. Open [http://localhost:3000](http://localhost:3000)

## Development with TDD

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run tests with UI
npm run test:ui
```

### TDD Workflow

1. Write a failing test
2. Run the test: `npm test`
3. Implement the minimum code to pass
4. Refactor
5. Repeat

### Test Structure

```
tests/
├── setup.ts              # Test setup (jest-dom matchers)
├── unit/
│   ├── supabase.test.ts  # Supabase client tests
│   ├── stripe.test.ts    # Stripe client tests
│   ├── Dashboard.test.tsx # Dashboard component tests
│   └── Chat.test.tsx     # Chat component tests
└── integration/
    └── api.test.ts       # API routes integration tests
```

## Project Structure

```
boilerplate-saas/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth/route.ts     # Auth API endpoint
│   │   │   ├── billing/route.ts  # Billing API endpoint
│   │   │   └── chat/route.ts     # Chat API endpoint
│   │   ├── globals.css           # Global Tailwind styles
│   │   ├── layout.tsx            # Root layout
│   │   └── page.tsx              # Home page
│   ├── components/
│   │   ├── Dashboard.tsx         # Dashboard stats component
│   │   └── Chat.tsx              # AI chat component
│   └── lib/
│       ├── supabase.ts           # Supabase client singleton
│       └── stripe.ts             # Stripe client singleton
├── tests/                        # Test files
├── .github/workflows/ci.yml      # CI/CD pipeline
├── next.config.js                # Next.js configuration
├── tailwind.config.ts            # Tailwind configuration
├── tsconfig.json                 # TypeScript configuration
├── vitest.config.ts              # Vitest configuration
└── package.json                  # Dependencies and scripts
```

## API Endpoints

### `POST /api/auth`
Login with email/password.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### `DELETE /api/auth`
Logout current user.

### `POST /api/billing`
Create a payment intent.

**Body:**
```json
{
  "customerId": "cus_xxx",
  "amount": 2000,
  "currency": "usd",
  "description": "Pro plan"
}
```

### `GET /api/billing?customerId=cus_xxx`
Get billing history for a customer.

### `POST /api/chat`
Send messages to AI assistant.

**Body:**
```json
{
  "messages": [
    { "role": "user", "content": "Hello!" }
  ],
  "model": "gpt-4o-mini",
  "stream": false
}
```

## Docker Compose (Local Supabase)

```yaml
# docker-compose.yml (run Supabase locally)
services:
  supabase:
    image: supabase/supabase-local:latest
    ports:
      - "54321:54321"
      - "54322:54322"
    env_file:
      - .env.local
```

## CI/CD Pipeline

The GitHub Actions workflow runs on every push and PR:

1. **Lint & Type Check** - ESLint + TypeScript
2. **Test** - Vitest with coverage
3. **Build** - Next.js production build
4. **Deploy** - Configure for your platform (Vercel, AWS, etc.)

## Environment Variables

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key |
| `STRIPE_SECRET_KEY` | Stripe secret key |
| `OPENAI_API_KEY` | OpenAI API key |

## License

MIT