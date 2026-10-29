# WY Wallet

**by: wromly**

Telegram Mini App wallet based on the GPL-licensed MyTonWallet **26.9.5** source (commit `781e2054aaeb8463ba08c1631544d237a8106144`). Independent branding, original WY logo, and open source code. The upstream application logic is retained; the WY changes are not independently audited.

App: https://wromlyy.github.io/wy-wallet/

## Build

Use Node.js 24 and npm 11.

```sh
ELECTRON_SKIP_BINARY_DOWNLOAD=1 PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
npm run telegram:dev
npm run telegram:build:production
```

The production site is generated in `dist/`. Serve this directory over HTTPS. All assets use relative paths so the Mini App can run from a GitHub Pages project directory.

## GitHub Pages

The `WY Wallet Mini App` workflow type-checks, builds the Telegram version, attaches the finished site as an artifact and deploys to Pages. In repository **Settings → Pages → Source**, select **GitHub Actions**. Push to `main` or run the workflow manually.

## Connect Telegram

1. Create a bot in [@BotFather](https://t.me/BotFather), or select your existing bot.
2. Set its visible name to **WY Wallet**, description to **WY Wallet · by: wromly**, and bot avatar to `public/icon-512x512.png`.
3. Open **Bot Settings → Configure Mini App → Enable Mini App**, and enter `https://wromlyy.github.io/wy-wallet/` as the Main Mini App URL.
4. Set the menu button to the same HTTPS URL, with text **WY Wallet**.
5. Open the app using the bot's **Open App** button.

No bot token is needed to build or host this client. Never put a bot token or a seed phrase in repository variables or frontend code. `BOT_USERNAME` is an optional upstream diesel-service integration, not a requirement for launching a Mini App; leave it empty unless a compatible backend is configured.

Telegram initialization, themes, viewport/safe-area handling, back navigation and biometric support come from the upstream Telegram build. See [Telegram Mini Apps documentation](https://core.telegram.org/bots/webapps).

## Scope and external services

The Mini App retains upstream blockchain RPC, swap, staking and other service integrations. Some features depend on upstream APIs, CORS permissions, credentials or additional server components. The project includes no replacement backend and does not claim all upstream services will work for an independent deployment. Use a newly created test wallet for verification; no real-money transaction was used to validate the build.

`public/logo.svg` is the editable vector logo. `python3 dev/createWyLogo.py` regenerates app icons with Pillow. Original native Android/iOS/Electron sources are kept for reference; this workflow builds the Telegram web app only.

## License and attribution

[GNU GPL v3](LICENSE). Original copyright holders: MyTonWallet contributors. WY Wallet branding and Mini App packaging modified by wromly on 2026-10-29. [Upstream details](UPSTREAM.md). Provided without warranty. Later source-available upstream releases are not incorporated.
