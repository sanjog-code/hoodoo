const fs = require('fs');
const d = JSON.parse(fs.readFileSync('forensic_audit_dump.json', 'utf8'));

console.log('=== NETWORK & RUNTIME LOGS ===');
console.log('Console Errors:', d.logs.consoleErrors.length, d.logs.consoleErrors);
console.log('Console Warnings:', d.logs.consoleWarnings.length);
console.log('Page Errors:', d.logs.pageErrors.length, d.logs.pageErrors);
console.log('Network 4xx/5xx Errors:', d.logs.networkErrors.length, d.logs.networkErrors);

console.log('\n=== INTERACTION TRIALS ===');
console.log(JSON.stringify(d.trials, null, 2));

console.log('\n=== CONTROLS AUDIT ===');
const controls = d.domAudit.controls;
console.log('Total interactive controls detected:', controls.length);
const visible = controls.filter(c => c.isVisible);
console.log('Visible interactive controls:', visible.length);

const sub32 = visible.filter(c => c.touchSub32);
console.log('\n--- Sub-32px Targets (' + sub32.length + ') ---');
sub32.forEach((c, i) => console.log(`${i+1}. [${c.tag}] "${c.text}" (${c.width}x${c.height}px) class: "${c.className}" id: "${c.id}"`));

const sub44 = visible.filter(c => c.touchSub44 && !c.touchSub32);
console.log('\n--- Sub-44px Targets (32px-43px) (' + sub44.length + ') ---');
sub44.forEach((c, i) => console.log(`${i+1}. [${c.tag}] "${c.text}" (${c.width}x${c.height}px) class: "${c.className}"`));

const lowContrast = visible.filter(c => c.contrast !== null && c.contrast < 4.5);
console.log('\n--- Low Contrast Controls (<4.5:1) (' + lowContrast.length + ') ---');
lowContrast.forEach((c, i) => console.log(`${i+1}. [${c.tag}] "${c.text}" contrast: ${c.contrast}:1 (fg: ${c.color}, bg: ${c.bgColor})`));

const noAriaOrText = visible.filter(c => !c.hasAria && (!c.text || c.text.length === 0));
console.log('\n--- Controls without accessible name / text (' + noAriaOrText.length + ') ---');
noAriaOrText.forEach((c, i) => console.log(`${i+1}. [${c.tag}] id: "${c.id}" class: "${c.className}"`));

console.log('\n=== IMAGES AUDIT ===');
console.log('Total Images:', d.domAudit.images.length);
const brokenImages = d.domAudit.images.filter(img => !img.complete || img.naturalWidth === 0);
console.log('Broken/Unloaded Images:', brokenImages.length, brokenImages);
const missingAlt = d.domAudit.images.filter(img => !img.alt || img.alt.trim() === '');
console.log('Images missing Alt text:', missingAlt.length);
missingAlt.slice(0, 5).forEach(img => console.log('  Missing alt:', img.src));
