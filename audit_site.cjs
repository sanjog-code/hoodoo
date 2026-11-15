const { chromium } = require('playwright');
const fs = require('fs');

async function runForensicAudit() {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 }
  });
  const page = await context.newPage();

  const logs = {
    consoleErrors: [],
    consoleWarnings: [],
    pageErrors: [],
    networkErrors: []
  };

  page.on('console', msg => {
    if (msg.type() === 'error') logs.consoleErrors.push(msg.text());
    if (msg.type() === 'warning') logs.consoleWarnings.push(msg.text());
  });
  page.on('pageerror', err => logs.pageErrors.push(err.toString()));
  page.on('response', resp => {
    if (resp.status() >= 400) {
      logs.networkErrors.push({ url: resp.url(), status: resp.status() });
    }
  });

  console.log('Navigating to http://localhost:8000...');
  await page.goto('http://localhost:8000', { waitUntil: 'networkidle' });

  // Evaluate DOM and controls
  const domAudit = await page.evaluate(() => {
    function parseRgb(colorStr) {
      const match = colorStr.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
      if (!match) return null;
      return {
        r: parseInt(match[1]),
        g: parseInt(match[2]),
        b: parseInt(match[3]),
        a: match[4] !== undefined ? parseFloat(match[4]) : 1
      };
    }

    function getLuminance(r, g, b) {
      const a = [r, g, b].map(v => {
        v /= 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
      });
      return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
    }

    function getContrast(rgb1, rgb2) {
      if (!rgb1 || !rgb2) return null;
      const l1 = getLuminance(rgb1.r, rgb1.g, rgb1.b);
      const l2 = getLuminance(rgb2.r, rgb2.g, rgb2.b);
      const brightest = Math.max(l1, l2);
      const darkest = Math.min(l1, l2);
      return (brightest + 0.05) / (darkest + 0.05);
    }

    const interactiveSelector = 'button, a, input, select, textarea, [role="button"], [tabindex]:not([tabindex="-1"])';
    const elements = Array.from(document.querySelectorAll(interactiveSelector));

    const controls = elements.map(el => {
      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);
      const tag = el.tagName.toLowerCase();
      const text = (el.innerText || el.getAttribute('aria-label') || el.getAttribute('placeholder') || el.value || '').trim();
      const ariaLabel = el.getAttribute('aria-label');
      const hasAria = !!(ariaLabel || el.getAttribute('aria-labelledby') || el.getAttribute('aria-describedby'));
      const id = el.id || '';
      const className = (el.className || '').toString();

      const colorRgb = parseRgb(style.color);
      let bg = style.backgroundColor;
      let parent = el.parentElement;
      while (parent && (bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent')) {
        bg = window.getComputedStyle(parent).backgroundColor;
        parent = parent.parentElement;
      }
      const bgRgb = parseRgb(bg) || { r: 12, g: 12, b: 11, a: 1 }; // default dark bg
      const contrast = getContrast(colorRgb, bgRgb);

      const isVisible = rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none' && style.opacity !== '0';
      const touchSub32 = isVisible && (rect.width < 32 || rect.height < 32);
      const touchSub44 = isVisible && (rect.width < 44 || rect.height < 44);

      return {
        tag,
        text: text.slice(0, 50),
        id,
        className: className.slice(0, 50),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
        isVisible,
        touchSub32,
        touchSub44,
        hasAria,
        ariaLabel,
        color: style.color,
        bgColor: bg,
        contrast: contrast ? Math.round(contrast * 10) / 10 : null,
        cursor: style.cursor,
        outline: style.outline
      };
    });

    // Check headings hierarchy
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => ({
      tag: h.tagName.toLowerCase(),
      text: h.innerText.slice(0, 40)
    }));

    return {
      controls,
      headings,
      images: Array.from(document.querySelectorAll('img')).map(img => ({
        src: img.src,
        alt: img.alt,
        complete: img.complete,
        naturalWidth: img.naturalWidth
      }))
    };
  });

  // Feature interaction trials
  const trials = {};

  // Test 1: Category filter clicking
  try {
    const filterBtns = await page.$$('.filter-pill, .cat-btn, [data-category]');
    trials.categoryFilters = { found: filterBtns.length, clicksWorking: false };
    if (filterBtns.length > 1) {
      await filterBtns[1].click();
      await page.waitForTimeout(200);
      trials.categoryFilters.clicksWorking = true;
    }
  } catch (e) {
    trials.categoryFilters = { error: e.message };
  }

  // Test 2: Add to cart
  try {
    const addBtn = await page.$('.btn-add-to-cart, button:has-text("Acquire"), button:has-text("Add to Bag")');
    trials.addToCart = { found: !!addBtn, executed: false, badgeUpdated: false };
    if (addBtn) {
      await addBtn.click();
      await page.waitForTimeout(300);
      trials.addToCart.executed = true;
      const countEl = await page.$('#cart-count-badge, .cart-count, [data-count]');
      if (countEl) {
        trials.addToCart.badgeUpdated = (await countEl.innerText()).trim();
      }
    }
  } catch (e) {
    trials.addToCart = { error: e.message };
  }

  // Test 3: Cart Drawer open / close
  try {
    const cartToggle = await page.$('#nav-cart-btn, [aria-label="Open Cart"], .cart-toggle');
    trials.cartDrawer = { foundToggle: !!cartToggle, opened: false, closed: false };
    if (cartToggle) {
      await cartToggle.click();
      await page.waitForTimeout(300);
      const drawer = await page.$('#cart-drawer, .cart-drawer, [aria-label="Shopping Cart"]');
      if (drawer && await drawer.isVisible()) {
        trials.cartDrawer.opened = true;
        const closeBtn = await page.$('#cart-close-btn, .cart-drawer-close, [aria-label="Close cart"]');
        if (closeBtn) {
          await closeBtn.click();
          await page.waitForTimeout(300);
          trials.cartDrawer.closed = !(await drawer.isVisible());
        }
      }
    }
  } catch (e) {
    trials.cartDrawer = { error: e.message };
  }

  // Test 4: Commission Form Calculator
  try {
    const lengthInput = await page.$('#dim-length, input[name="length"]');
    const widthInput = await page.$('#dim-width, input[name="width"]');
    trials.calculator = { inputsFound: !!(lengthInput && widthInput), recalculated: false };
    if (lengthInput && widthInput) {
      const priceBefore = await page.$eval('#quote-price-display, .quote-total', el => el.innerText).catch(() => null);
      await lengthInput.fill('96');
      await widthInput.fill('42');
      await page.waitForTimeout(200);
      const priceAfter = await page.$eval('#quote-price-display, .quote-total', el => el.innerText).catch(() => null);
      trials.calculator.recalculated = priceBefore !== priceAfter;
      trials.calculator.priceBefore = priceBefore;
      trials.calculator.priceAfter = priceAfter;
    }
  } catch (e) {
    trials.calculator = { error: e.message };
  }

  // Test 5: Keyboard Tab Navigation Focus
  try {
    await page.keyboard.press('Tab');
    const activeTagName = await page.evaluate(() => document.activeElement ? document.activeElement.tagName : null);
    trials.keyboardTab = { firstActive: activeTagName };
  } catch (e) {
    trials.keyboardTab = { error: e.message };
  }

  const results = {
    logs,
    domAudit,
    trials
  };

  fs.writeFileSync('forensic_audit_dump.json', JSON.stringify(results, null, 2));
  console.log('FORENSIC_AUDIT_DATA_DUMPED');
  await browser.close();
}

runForensicAudit().catch(err => {
  console.error('Forensic audit failed:', err);
  process.exit(1);
});
