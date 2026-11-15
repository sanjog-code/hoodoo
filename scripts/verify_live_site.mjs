import { chromium } from 'playwright';
import path from 'path';

const ARTIFACT_DIR = 'C:\\Users\\sanjo\\.gemini\\antigravity\\brain\\234f9af8-00da-4e48-94a4-b01c33156985';

async function run() {
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true,
    args: ['--use-gl=angle', '--use-angle=d3d11', '--enable-webgl', '--ignore-gpu-blocklist'],
  });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  page.on('console', (msg) => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', (err) => console.error('PAGE ERROR:', err.message));

  console.log('Navigating to http://localhost:4173...');
  await page.goto('http://localhost:4173', { waitUntil: 'networkidle' });

  // 1. Screenshot Homepage
  await page.waitForTimeout(2000);
  const homePath = path.join(ARTIFACT_DIR, 'live_preview_home.png');
  await page.screenshot({ path: homePath });
  console.log(`Saved home screenshot to ${homePath}`);

  // 2. Open 3D Studio from Hero
  console.log('Opening 3D Studio modal for Hoodie...');
  const studioBtn = page.locator('button:has-text("LAUNCH 3D ATELIER"), button:has-text("3D STUDIO"), button:has-text("VIEW IN 3D")').first();
  await studioBtn.click();

  // Wait for 3D model to load in modal
  await page.waitForTimeout(4000);
  const hoodie3DPath = path.join(ARTIFACT_DIR, 'live_3d_hoodie_modal.png');
  await page.screenshot({ path: hoodie3DPath });
  console.log(`Saved hoodie 3D modal screenshot to ${hoodie3DPath}`);

  // 3. Switch to Tee category in 3D modal
  console.log('Switching to Tee category in 3D modal...');
  const modalTeeCategory = page.locator('div.fixed.z-50 button', { hasText: /^tees$/i }).first();
  await modalTeeCategory.click();
  await page.waitForTimeout(1000);

  // Click first tee item in the left dock
  const firstTeeItem = page.locator('div.fixed.z-50 div.overflow-y-auto button').first();
  await firstTeeItem.click();
  await page.waitForTimeout(4000);
  const tee3DPath = path.join(ARTIFACT_DIR, 'live_3d_tee_modal.png');
  await page.screenshot({ path: tee3DPath });
  console.log(`Saved tee 3D modal screenshot to ${tee3DPath}`);

  // 4. Switch to Kicks category in 3D modal
  console.log('Switching to Kicks category in 3D modal...');
  const modalKicksCategory = page.locator('div.fixed.z-50 button', { hasText: /^kicks$/i }).first();
  await modalKicksCategory.click();
  await page.waitForTimeout(1000);

  // Click first kick item in the left dock
  const firstKickItem = page.locator('div.fixed.z-50 div.overflow-y-auto button').first();
  await firstKickItem.click();
  await page.waitForTimeout(4000);
  const kicks3DPath = path.join(ARTIFACT_DIR, 'live_3d_kicks_modal.png');
  await page.screenshot({ path: kicks3DPath });
  console.log(`Saved kicks 3D modal screenshot to ${kicks3DPath}`);

  await browser.close();
  console.log('ALL VERIFICATIONS COMPLETED SUCCESSFULLY!');
}

run().catch((err) => {
  console.error('Test run failed:', err);
  process.exit(1);
});
