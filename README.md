# Invest KI — AI Trading Agents

AI-powered stock research and trading agents built with Claude + Alpaca.

## Structure

```
agents/       # Agent logic (analysis, strategies)
api/          # Vercel serverless functions (triggered by cron)
config/       # Watchlists and settings
utils/        # Shared helper functions
```

## Setup

1. Clone this repo
2. Copy `.env.example` to `.env` and fill in your keys
3. Install dependencies: `pip install -r requirements.txt`

## Environment Variables

- `ALPACA_API_KEY` — Alpaca paper trading key
- `ALPACA_SECRET_KEY` — Alpaca secret key
- `ANTHROPIC_API_KEY` — Claude API key (for agent reasoning)

## Deployment

Connected to Vercel — every push to `main` deploys automatically.
