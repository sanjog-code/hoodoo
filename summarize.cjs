const fs = require('fs');
let buf = fs.readFileSync('electronics-ecommerce-store/re_audit.json');
let str;
if (buf[0] === 0xff && buf[1] === 0xfe) {
  str = buf.toString('utf16le');
} else if (buf[0] === 0xfe && buf[1] === 0xff) {
  str = buf.toString('utf16be');
} else {
  str = buf.toString('utf8');
}

const marker = '--- FULL AUDIT DATA ---';
const idx = str.indexOf(marker);
const jsonPart = str.slice(idx + marker.length).trim();
const d = JSON.parse(jsonPart);

for (const [name, p] of Object.entries(d.pages)) {
  console.log(`\n========================================`);
  console.log(`PAGE: ${name} (${p.url})`);
  console.log(`Controls: Total ${p.totalControls} | Dead: ${p.deadControls.length} | Hidden: ${p.hiddenControls.length} | Small: ${p.smallTargetControls.length}`);
  console.log(`Errors: PageErrors=${p.pageErrors.length}, FailedReqs=${p.failed404s.length}`);
  console.log(`Broken/NoAlt Images: ${p.brokenImages.length}`);
  console.log(`3D Canvas:`, p.threeStatus);
  console.log(`Video Canvas:`, p.videoStatus);
  if (p.contrastViolations.length) {
    console.log(`Contrast Violations (${p.contrastViolations.length}):`, p.contrastViolations);
  }
}
