// Run the real production bundle at a subdirectory, as on GitHub Pages.
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { readFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { chromium, expect } from '@playwright/test';

const root = path.resolve('dist');
const mime = {
  '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp', '.wasm': 'application/wasm',
  '.woff': 'font/woff', '.woff2': 'font/woff2', '.webmanifest': 'application/manifest+json',
};
const server = createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  if (!url.pathname.startsWith('/wy-wallet/')) { res.writeHead(404).end(); return; }
  const filename = path.resolve(root, decodeURIComponent(url.pathname.slice('/wy-wallet/'.length)) || 'index.html');
  if (!filename.startsWith(`${root}/`)) { res.writeHead(403).end(); return; }
  try {
    const body = await readFile(filename);
    res.writeHead(200, { 'Content-Type': mime[path.extname(filename)] || 'application/octet-stream' });
    res.end(body);
  } catch { res.writeHead(404).end(); }
});
await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const browser = await chromium.launch();
try {
  await mkdir('test-results/wy-miniapp', { recursive: true });
  for (const colorScheme of ['light', 'dark']) {
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 }, deviceScaleFactor: 1,
      isMobile: true, hasTouch: true, locale: 'en-US', colorScheme,
    });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', (error) => errors.push(error.message));
    try {
    await page.goto(`http://127.0.0.1:${server.address().port}/wy-wallet/`, { waitUntil: 'domcontentloaded' });
    await page.getByText('by: wromly', { exact: true }).waitFor({ timeout: 60000 });
    assert.equal(await page.title(), 'WY Wallet');
    const logo = page.getByRole('img', { name: 'WY Wallet', exact: true });
    await logo.waitFor();
    assert.equal(await logo.evaluate((img) => img.complete && img.naturalWidth > 0), true);
    const createButton = page.getByRole('button', { name: 'Create New Wallet', exact: true });
    assert.equal(await createButton.isDisabled(), true, 'Terms must be accepted before creating a wallet');
    await page.getByRole('checkbox').press('Space');
    await expect(createButton).toBeEnabled();
    assert.deepEqual(errors, [], 'Application must start without uncaught errors');
    console.log(`${colorScheme}: production bundle boots under /wy-wallet/, branding and onboarding gate verified`);
    } finally {
      await page.screenshot({ path: `test-results/wy-miniapp/${colorScheme}.png`, fullPage: true });
      await context.close();
    }
  }
} finally {
  await browser.close();
  server.close();
}
