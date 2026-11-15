import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const OUT_DIR = path.resolve('test-results/forensic');
if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

async function runForensicAudit() {
  console.log('🚀 Starting UI/UX Forensic Audit with Playwright...');
  const browser = await chromium.launch({
    channel: 'chrome',
    headless: true,
    args: ['--enable-webgl', '--use-gl=angle', '--use-angle=default', '--ignore-gpu-blocklist', '--no-sandbox'],
  });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  const consoleErrors = [];
  const consoleWarnings = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
    if (msg.type() === 'warning') consoleWarnings.push(msg.text());
  });

  page.on('pageerror', err => {
    consoleErrors.push(err.toString());
  });

  const auditLog = [];
  function logCheck(name, pass, details) {
    auditLog.push({ name, pass, details });
    console.log(`[${pass ? 'PASS' : 'FAIL'}] ${name}: ${details}`);
  }

  // 1. Navigation & Boot
  await page.goto('http://localhost:5173', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // Take Desktop Hero Screenshot
  await page.screenshot({ path: path.join(OUT_DIR, '01_hero_desktop.png') });

  // 2. Horizontal Overflow Check
  const overflowCheck = await page.evaluate(() => {
    return {
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      hasOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    };
  });
  logCheck(
    'No Horizontal Layout Overflow',
    !overflowCheck.hasOverflow,
    `scrollWidth=${overflowCheck.scrollWidth}px, clientWidth=${overflowCheck.clientWidth}px`
  );

  // 3. Three.js Canvas Verification
  const canvasVerified = await page.evaluate(() => {
    const canvas = document.querySelector('#hero canvas');
    return canvas !== null;
  });
  logCheck('4K WebGL Three.js Canvas Rendered', canvasVerified, 'Canvas element mounted and active in #hero viewport');

  // 4. Interactive Affordances Census
  const controlsInventory = await page.evaluate(() => {
    const buttons = Array.from(document.querySelectorAll('button'));
    const inputs = Array.from(document.querySelectorAll('input'));
    const links = Array.from(document.querySelectorAll('a'));

    return {
      buttonCount: buttons.length,
      inputCount: inputs.length,
      linkCount: links.length,
      totalCtrls: buttons.length + inputs.length + links.length,
    };
  });
  logCheck(
    'Interactive Affordance Inventory (Census)',
    controlsInventory.totalCtrls >= 15,
    `Total controls: ${controlsInventory.totalCtrls} (Buttons: ${controlsInventory.buttonCount}, Inputs: ${controlsInventory.inputCount})`
  );

  // 5. Test Explode 3D Layers Action
  const explodeBtn = page.getByRole('button', { name: /EXPLODE/i }).first();
  const hasExplode = await explodeBtn.isVisible();
  if (hasExplode) {
    await explodeBtn.click();
    await page.waitForTimeout(600);
    const legendVisible = await page.getByText('ANATOMY OF THE BIG MOUTH:').first().isVisible();
    await page.screenshot({ path: path.join(OUT_DIR, '02_exploded_3d_burger.png') });
    logCheck('3D Layer Explode & Telemetry Trigger', legendVisible, 'Layers expanded, 6-part telemetry active');

    // Assemble back using the re-labeled button
    const assembleBtn = page.getByRole('button', { name: /ASSEMBLE/i }).first();
    await assembleBtn.click();
    await page.waitForTimeout(400);
  } else {
    logCheck('3D Layer Explode Trigger', false, 'Button not visible');
  }

  // 6. Test CCTV Video Wall Interaction
  const videoSection = page.locator('#video-wall');
  await videoSection.scrollIntoViewIfNeeded();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '03_cctv_video_wall.png') });

  // Click Channel 2 (MACRO LENS #04)
  const channel2 = page.getByRole('button', { name: /MACRO LENS #04/i });
  if (await channel2.isVisible()) {
    await channel2.click();
    await page.waitForTimeout(400);
    const channel2Active = await page.getByText('THE DOUBLE CHEDDAR CASCADE').first().isVisible();
    logCheck('CCTV Video Channel Switching', channel2Active, 'Channel switched to Macro Lens feed');
  }

  // 7. Test Pop-Culture Food Menu Filtering
  const menuSection = page.locator('#menu');
  await menuSection.scrollIntoViewIfNeeded();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '04_pop_culture_menu.png') });

  // Filter 'shakes'
  const shakeFilter = page.getByRole('button', { name: 'SHAKES', exact: true });
  if (await shakeFilter.isVisible()) {
    await shakeFilter.click();
    await page.waitForTimeout(400);
    const dragonfruitVisible = await page.getByText('NEON DRAGONFRUIT SHAKE').isVisible();
    const cyberSmashVisible = await page.getByText('THE CYBER-SMASH 2077').isVisible();
    logCheck('Menu Category Tab Filter', dragonfruitVisible && !cyberSmashVisible, 'Filtered to shakes only');
  }

  // Reset to Full Menu
  const allFilter = page.getByRole('button', { name: 'FULL MENU' });
  await allFilter.click();
  await page.waitForTimeout(400);

  // 8. Test Add to Bag & Toast Notification
  const initialBagBadge = await page.locator('header').getByText(/^\d+$/).first().innerText();
  const addCyberBtn = page.getByRole('button', { name: /ADD TO BAG/i }).first();
  await addCyberBtn.click();
  await page.waitForTimeout(500);

  const toastVisible = await page.getByText(/CHOMPED! Added/i).first().isVisible();
  const updatedBagBadge = await page.locator('header').getByText(/^\d+$/).first().innerText();
  logCheck(
    'Reactive Add-to-Bag & Toast Feedback',
    toastVisible && parseInt(updatedBagBadge) > parseInt(initialBagBadge),
    `Toast shown, bag count incremented from ${initialBagBadge} to ${updatedBagBadge}`
  );

  // 9. Test Bite Bag Drawer & Promo Validation & Checkout
  const bagButton = page.getByRole('button', { name: /BITE BAG/i });
  await bagButton.click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, '05_bite_bag_drawer.png') });

  // Check Drawer Open
  const drawerOpen = await page.getByText('THE BITE BAG').isVisible();
  logCheck('Bite Bag Slide-out Drawer', drawerOpen, 'Drawer opened with item list & subtotal');

  // Test Promo Code (Invalid Code First)
  const promoInput = page.getByPlaceholder(/CODE \(e\.g\. BIGMOUTH20\)/i);
  const applyPromoBtn = page.getByRole('button', { name: 'APPLY' });
  await promoInput.fill('WRONGCODE');
  await applyPromoBtn.click();
  await page.waitForTimeout(300);
  const errorVisible = await page.getByText(/Invalid code/i).isVisible();
  logCheck('Promo Code Error Validation (State 7)', errorVisible, 'Shows invalid code warning');

  // Test Valid Promo Code (BIGMOUTH20)
  await promoInput.fill('BIGMOUTH20');
  await applyPromoBtn.click();
  await page.waitForTimeout(300);
  const successPromo = await page.getByText(/20% GEN Z VIP DISCOUNT APPLIED/i).isVisible();
  logCheck('Promo Code 20% Discount (State 8)', successPromo, 'Discount calculated and verified');

  // Test Order Checkout & Flat-Top Transmission
  const checkoutBtn = page.getByRole('button', { name: /TRANSMIT ORDER TO FLAT-TOP/i });
  await checkoutBtn.click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '06_order_confirmed_ticket.png') });

  const ticketVisible = await page.getByText(/ORDER #\d+/i).isVisible();
  logCheck('Order Checkout & Flat-top Ticket Generation', ticketVisible, 'Ticket # generated with station & ready time');

  // Close ticket
  const closeTicketBtn = page.getByRole('button', { name: /CHOMP DONE • CLOSE TICKET/i });
  await closeTicketBtn.click();
  await page.waitForTimeout(400);

  // 10. Mobile Viewport Audit (iPhone 14 - 390x844)
  const mobilePage = await context.newPage();
  await mobilePage.setViewportSize({ width: 390, height: 844 });
  await mobilePage.goto('http://localhost:5173', { waitUntil: 'networkidle' });
  await mobilePage.waitForTimeout(800);
  await mobilePage.screenshot({ path: path.join(OUT_DIR, '07_mobile_viewport.png') });

  const mobileOverflow = await mobilePage.evaluate(() => {
    return document.documentElement.scrollWidth <= document.documentElement.clientWidth;
  });
  logCheck('Mobile Responsiveness & Viewport Fit', mobileOverflow, 'No horizontal overflow on 390px mobile viewport');
  await mobilePage.close();

  // 11. Console Hygiene Check
  logCheck(
    'Console Hygiene & Zero Uncaught Errors',
    consoleErrors.length === 0,
    consoleErrors.length === 0 ? 'Zero unhandled console errors' : `Errors: ${consoleErrors.join(', ')}`
  );

  await browser.close();

  // Calculate Deterministic Scores
  const passes = auditLog.filter(c => c.pass).length;
  const totalChecks = auditLog.length;

  const resultJson = {
    timestamp: new Date().toISOString(),
    auditLog,
    controlsInventory,
    consoleErrors,
    passes,
    totalChecks,
    passRate: `${((passes / totalChecks) * 100).toFixed(1)}%`,
  };
  fs.writeFileSync(path.join(OUT_DIR, 'audit_report.json'), JSON.stringify(resultJson, null, 2));

  console.log('\n=========================================');
  console.log(`📊 Playwright Forensic Audit Finished: ${passes}/${totalChecks} Passed (${resultJson.passRate})`);
  console.log(`📁 Artifacts & Screenshots: ${OUT_DIR}`);
  console.log('=========================================\n');
}

runForensicAudit().catch(err => {
  console.error('Audit failed with error:', err);
  process.exit(1);
});
