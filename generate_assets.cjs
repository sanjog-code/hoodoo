const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'electronics-ecommerce-store', 'assets');
if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

function wrapSvg(title, subtitle, graphicContent) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" height="100%">
  <defs>
    <linearGradient id="gridGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#141A22"/>
      <stop offset="100%" stop-color="#0B0E14"/>
    </linearGradient>
    <pattern id="diagGrid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 40 M 0 0 L 40 40" fill="none" stroke="#161D27" stroke-width="0.75"/>
    </pattern>
    <linearGradient id="cyanGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00D2FF"/>
      <stop offset="100%" stop-color="#00F298"/>
    </linearGradient>
  </defs>
  <rect width="800" height="500" fill="url(#gridGrad)"/>
  <rect width="800" height="500" fill="url(#diagGrid)" opacity="0.6"/>
  <!-- Perimeter Engineering Frame -->
  <rect x="24" y="24" width="752" height="452" rx="8" fill="none" stroke="#222B3A" stroke-width="1.2"/>
  <!-- Corner Crosshairs -->
  <path d="M 20 24 L 28 24 M 24 20 L 24 28" stroke="#00F298" stroke-width="1.5"/>
  <path d="M 772 24 L 780 24 M 776 20 L 776 28" stroke="#00F298" stroke-width="1.5"/>
  <path d="M 20 476 L 28 476 M 24 472 L 24 480" stroke="#00F298" stroke-width="1.5"/>
  <path d="M 772 476 L 780 476 M 776 472 L 776 480" stroke="#00F298" stroke-width="1.5"/>
  <!-- Header Telemetry -->
  <text x="44" y="54" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#00F298" letter-spacing="0.1em">${title.toUpperCase()}</text>
  <text x="756" y="54" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="10" fill="#718096" letter-spacing="0.05em">SPEC ARCHITECTURE // VERIFIED</text>
  <!-- Main Graphical Content -->
  ${graphicContent}
  <!-- Footer Telemetry -->
  <text x="44" y="456" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="600" fill="#E2E8F0">${subtitle}</text>
  <text x="756" y="456" text-anchor="end" font-family="'JetBrains Mono', monospace" font-size="10" fill="#00D2FF">100% MODULAR &amp; SUSTAINABLE</text>
</svg>`;
}

const assets = {
  'razerclip-alpha.svg': wrapSvg(
    'Razerclip 15 Alpha // Rev 2026',
    'CNC Post-Consumer Aluminum • 144Hz IPS • Modular SO-DIMM',
    `<!-- Laptop Chassis Vector -->
    <g transform="translate(180, 110)">
      <!-- Base Deck -->
      <polygon points="40,240 400,240 440,265 0,265" fill="#1A222E" stroke="#2D3A4D" stroke-width="2"/>
      <rect x="150" y="248" width="140" height="12" rx="2" fill="#0B0E14" stroke="#00F298" stroke-width="1"/>
      <!-- Trackpad -->
      <rect x="170" y="210" width="100" height="25" rx="3" fill="#141A24" stroke="#2A3648" stroke-width="1"/>
      <!-- Keyboard Grid -->
      <rect x="70" y="145" width="300" height="60" rx="4" fill="#0E121A" stroke="#243040" stroke-width="1.2"/>
      <g fill="#18202D" stroke="#00F298" stroke-width="0.5" opacity="0.85">
        <rect x="76" y="150" width="288" height="10" rx="1"/>
        <rect x="76" y="163" width="288" height="10" rx="1"/>
        <rect x="76" y="176" width="288" height="10" rx="1"/>
        <rect x="76" y="189" width="288" height="12" rx="1"/>
      </g>
      <!-- Screen Lid Angle -->
      <polygon points="50,140 390,140 360,20 80,20" fill="#111620" stroke="#00F298" stroke-width="1.8"/>
      <!-- Display Panel -->
      <polygon points="62,132 378,132 350,30 90,30" fill="#07090E" stroke="#1F2A38" stroke-width="1"/>
      <circle cx="220" cy="80" r="28" fill="none" stroke="#00F298" stroke-width="2" stroke-dasharray="4 2"/>
      <text x="220" y="84" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#00D2FF">144Hz FHD</text>
    </g>`
  ),

  'razerclip-pro.svg': wrapSvg(
    'Razerclip 15 Pro // Stealth Edition',
    'Dual Copper Vapor Chamber • RTX 4060 115W TGP • 2.5K 165Hz',
    `<!-- Pro Laptop Chassis Vector -->
    <g transform="translate(180, 110)">
      <polygon points="35,240 405,240 445,268 -5,268" fill="#161C26" stroke="#00D2FF" stroke-width="1.5"/>
      <!-- Thermal Exhaust Fins Rear -->
      <line x1="60" y1="268" x2="140" y2="268" stroke="#00F298" stroke-width="4"/>
      <line x1="300" y1="268" x2="380" y2="268" stroke="#00F298" stroke-width="4"/>
      <!-- Keyboard Bed with Ambient Glow -->
      <rect x="65" y="142" width="310" height="65" rx="4" fill="#0B0E14" stroke="#2D3B4E" stroke-width="1.5"/>
      <rect x="72" y="148" width="296" height="52" rx="2" fill="#121822"/>
      <text x="220" y="178" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="12" fill="#00D2FF" letter-spacing="0.2em">PER-KEY RGB MATRIX</text>
      <!-- Screen Display -->
      <polygon points="45,138 395,138 365,15 75,15" fill="#090C12" stroke="#00D2FF" stroke-width="2"/>
      <polygon points="56,130 384,130 356,24 84,24" fill="#05070A"/>
      <text x="220" y="75" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="14" font-weight="800" fill="#00F298">165Hz QHD G-SYNC</text>
      <text x="220" y="95" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10" fill="#8898AA">RTX 4060 8GB GDDR6 // LIQUID METAL</text>
    </g>`
  ),

  'razerclip-max.svg': wrapSvg(
    'Razerclip 16 Max // Flagship Creator',
    'Intel Core i7-14700HX • 240Hz 16:10 QHD+ • 140W USB-C PD',
    `<!-- Max Creator Chassis Vector -->
    <g transform="translate(170, 100)">
      <polygon points="30,250 430,250 470,278 -10,278" fill="#121720" stroke="#00F298" stroke-width="2"/>
      <rect x="60" y="145" width="340" height="70" rx="4" fill="#0A0D14" stroke="#2A374A" stroke-width="1.5"/>
      <rect x="180" y="222" width="100" height="24" rx="3" fill="#18202C" stroke="#00F298" stroke-width="1"/>
      <!-- Screen 16:10 Tall Frame -->
      <polygon points="40,140 420,140 395,8 65,8" fill="#07090E" stroke="#00F298" stroke-width="2"/>
      <polygon points="50,132 410,132 388,16 72,16" fill="#040609"/>
      <circle cx="230" cy="74" r="32" fill="none" stroke="#00D2FF" stroke-width="2"/>
      <text x="230" y="72" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="800" fill="#F8FAFC">240Hz 16:10</text>
      <text x="230" y="88" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="#00F298">100% DCI-P3 500 NITS</text>
    </g>`
  ),

  'refurb-thinkpad.svg': wrapSvg(
    'ThinkPad X1 Carbon Gen 9 // Grade A+ Certified',
    'Ultrasonically Restored • Arctic MX-6 Applied • Certified 100% Battery',
    `<!-- ThinkPad Vector Blueprint -->
    <g transform="translate(190, 110)">
      <polygon points="35,240 385,240 420,265 0,265" fill="#101318" stroke="#333F50" stroke-width="2"/>
      <!-- Red TrackPoint -->
      <circle cx="210" cy="180" r="4" fill="#FF3333"/>
      <!-- Keyboard Structure -->
      <rect x="65" y="145" width="290" height="60" rx="3" fill="#090B0E" stroke="#263140" stroke-width="1"/>
      <!-- Classic ThinkPad Logo Stamp -->
      <text x="360" y="235" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" font-weight="800" fill="#E2E8F0">ThinkPad <tspan fill="#FF3333">i</tspan></text>
      <!-- Screen Frame -->
      <polygon points="45,140 375,140 350,20 70,20" fill="#0C0E12" stroke="#2D3847" stroke-width="1.8"/>
      <polygon points="55,132 365,132 342,28 78,28" fill="#06080B"/>
      <text x="210" y="75" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="700" fill="#00F298">GRADE A+ CERTIFIED</text>
      <text x="210" y="94" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10" fill="#94A3B8">1.13 KG CARBON FIBER // 400 NITS FHD+</text>
    </g>`
  ),

  'refurb-dell.svg': wrapSvg(
    'Dell XPS 15 9520 OLED // Grade A Certified',
    '3.5K OLED InfinityEdge • RTX 3050 Ti • Platinum Anodized Aluminum',
    `<!-- Dell XPS Vector Blueprint -->
    <g transform="translate(180, 110)">
      <polygon points="35,240 405,240 440,265 0,265" fill="#1A212B" stroke="#00D2FF" stroke-width="1.5"/>
      <rect x="160" y="212" width="120" height="26" rx="3" fill="#10151E" stroke="#2D3B4E" stroke-width="1"/>
      <rect x="65" y="142" width="310" height="62" rx="4" fill="#0B0E14" stroke="#263242" stroke-width="1.2"/>
      <!-- InfinityEdge Bezel-less Screen -->
      <polygon points="42,138 398,138 375,15 65,15" fill="#07090E" stroke="#00D2FF" stroke-width="2"/>
      <polygon points="46,134 394,134 372,19 68,19" fill="#030406"/>
      <circle cx="220" cy="74" r="30" fill="none" stroke="#00F298" stroke-width="1.5"/>
      <text x="220" y="73" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="800" fill="#F8FAFC">3.5K OLED</text>
      <text x="220" y="90" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="#00D2FF">TOUCH INFINITYEDGE // 100% DCI-P3</text>
    </g>`
  ),

  'refurb-asus.svg': wrapSvg(
    'ASUS ROG Zephyrus G14 // Grade A Certified',
    'AMD Ryzen 9 5900HS • RTX 3060 6GB • K5-Pro Restored Thermals',
    `<!-- Zephyrus Vector Blueprint -->
    <g transform="translate(190, 110)">
      <polygon points="30,240 390,240 425,268 -5,268" fill="#171D26" stroke="#FF5722" stroke-width="1.5"/>
      <rect x="60" y="145" width="300" height="60" rx="3" fill="#0C1017" stroke="#2B3648" stroke-width="1.2"/>
      <!-- Screen Lid with Dot Matrix Aesthetic -->
      <polygon points="40,140 380,140 355,20 65,20" fill="#0E121A" stroke="#FF5722" stroke-width="1.8"/>
      <polygon points="50,132 370,132 347,28 73,28" fill="#06080D"/>
      <text x="210" y="74" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="800" fill="#00F298">14.0" 120Hz WQHD</text>
      <text x="210" y="92" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10" fill="#FF5722">1.60 KG ULTRAPORTABLE BEAST</text>
    </g>`
  ),

  'part-cpu.svg': wrapSvg(
    'AMD Ryzen 7 7800X3D // Processor Architecture',
    'AM5 LGA Ceramic Heatspreader • 96MB 3D V-Cache • 5.0 GHz Boost',
    `<!-- CPU Architectural Vector -->
    <g transform="translate(260, 100)">
      <!-- PCB Substrate -->
      <rect x="0" y="0" width="280" height="280" rx="8" fill="#15261F" stroke="#00F298" stroke-width="2.5"/>
      <!-- Golden Alignment Dots & Corner Notch -->
      <circle cx="16" cy="16" r="4" fill="#E5C158"/>
      <circle cx="264" cy="16" r="3" fill="#E5C158"/>
      <circle cx="16" cy="264" r="3" fill="#E5C158"/>
      <circle cx="264" cy="264" r="3" fill="#E5C158"/>
      <!-- Nickel Plated Copper IHS -->
      <rect x="35" y="35" width="210" height="210" rx="6" fill="#1E2734" stroke="#485A74" stroke-width="2"/>
      <!-- Center Laser Inscription -->
      <text x="140" y="100" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="800" fill="#FF5722">AMD RYZEN™</text>
      <text x="140" y="130" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="800" fill="#00F298">7800X3D</text>
      <text x="140" y="160" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10" fill="#94A3B8">96MB 3D V-CACHE // 8-CORE 16-THREAD</text>
      <text x="140" y="180" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9" fill="#00D2FF">AM5 LGA // 120W TDP</text>
      <!-- Cap Cutouts -->
      <rect x="25" y="80" width="10" height="30" fill="#E5C158"/>
      <rect x="25" y="170" width="10" height="30" fill="#E5C158"/>
      <rect x="245" y="80" width="10" height="30" fill="#E5C158"/>
      <rect x="245" y="170" width="10" height="30" fill="#E5C158"/>
    </g>`
  ),

  'part-gpu.svg': wrapSvg(
    'NVIDIA GeForce RTX 4070 Super // Triple Axial-Tech',
    '12GB GDDR6X • DLSS 3.5 Frame Generation • Dual BIOS Fin-Stack',
    `<!-- GPU Vector Blueprint -->
    <g transform="translate(120, 110)">
      <!-- PCIe Gold Fingers -->
      <rect x="140" y="248" width="180" height="12" fill="#E5C158" stroke="#B89430" stroke-width="1"/>
      <rect x="70" y="254" width="40" height="6" fill="#E5C158"/>
      <!-- I/O Bracket -->
      <rect x="10" y="30" width="20" height="230" rx="3" fill="#2E3948" stroke="#4B5B72" stroke-width="1.5"/>
      <circle cx="20" cy="70" r="5" fill="#0B0E14"/>
      <circle cx="20" cy="110" r="5" fill="#0B0E14"/>
      <!-- Shroud & Fin Stack -->
      <rect x="30" y="30" width="520" height="215" rx="8" fill="#141922" stroke="#00D2FF" stroke-width="2"/>
      <!-- Triple Axial Fans -->
      <g stroke="#00F298" stroke-width="1.5" fill="#0B0E14">
        <!-- Fan 1 -->
        <circle cx="120" cy="135" r="60"/>
        <circle cx="120" cy="135" r="22" fill="#1A222E"/>
        <!-- Fan 2 -->
        <circle cx="290" cy="135" r="60"/>
        <circle cx="290" cy="135" r="22" fill="#1A222E"/>
        <!-- Fan 3 -->
        <circle cx="460" cy="135" r="60"/>
        <circle cx="460" cy="135" r="22" fill="#1A222E"/>
      </g>
      <text x="290" y="139" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#00F298">GEFORCE</text>
      <text x="290" y="220" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#E2E8F0">RTX 4070 SUPER 12GB GDDR6X</text>
    </g>`
  ),

  'part-ram.svg': wrapSvg(
    'Corsair Vengeance DDR5 // Dual Module Kit',
    '32GB (2x16GB) • 6000MT/s CL30-36-36-76 • Low Profile Anodized Heatspreader',
    `<!-- DDR5 Memory Module Vector -->
    <g transform="translate(120, 130)">
      <!-- Gold Connection Edge -->
      <rect x="20" y="210" width="520" height="15" fill="#E5C158" stroke="#B89430" stroke-width="1"/>
      <rect x="270" y="210" width="10" height="15" fill="#0B0E14"/>
      <!-- Anodized Black Heatspreader -->
      <rect x="15" y="40" width="530" height="170" rx="4" fill="#131821" stroke="#00F298" stroke-width="1.8"/>
      <!-- Micro-Fin Texture Top -->
      <g stroke="#263345" stroke-width="2">
        <line x1="30" y1="40" x2="30" y2="60"/>
        <line x1="60" y1="40" x2="60" y2="60"/>
        <line x1="90" y1="40" x2="90" y2="60"/>
        <line x1="120" y1="40" x2="120" y2="60"/>
        <line x1="440" y1="40" x2="440" y2="60"/>
        <line x1="470" y1="40" x2="470" y2="60"/>
        <line x1="500" y1="40" x2="500" y2="60"/>
        <line x1="530" y1="40" x2="530" y2="60"/>
      </g>
      <!-- Center Emblem Plate -->
      <rect x="160" y="80" width="240" height="70" rx="4" fill="#090C12" stroke="#00D2FF" stroke-width="1.2"/>
      <text x="280" y="112" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="#F8FAFC">VENGEANCE DDR5</text>
      <text x="280" y="134" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#00F298">6000MT/s CL30 // 32GB KIT</text>
    </g>`
  ),

  'proj-obsidian.svg': wrapSvg(
    'Project Obsidian // Stealth RTX 4090 Workstation',
    'Custom Hardline Matte Loop • Ryzen 9 7950X • 64GB DDR5 • 148 FPS 4K Ultra',
    `<!-- Custom Rig Showcase Vector -->
    <g transform="translate(230, 80)">
      <!-- Dual-Chamber Chassis -->
      <rect x="0" y="0" width="340" height="340" rx="10" fill="#0D1117" stroke="#00F298" stroke-width="2.5"/>
      <!-- Motherboard Tray -->
      <rect x="25" y="25" width="290" height="290" fill="#131A24" stroke="#263346" stroke-width="1.5"/>
      <!-- CPU Block with Custom Loop Tubing -->
      <rect x="120" y="70" width="70" height="70" rx="6" fill="#0A0D12" stroke="#00D2FF" stroke-width="2"/>
      <circle cx="155" cy="105" r="18" fill="none" stroke="#00F298" stroke-width="2"/>
      <!-- Matte Black Hardline Tubing -->
      <path d="M 155 70 L 155 35 L 290 35" fill="none" stroke="#00D2FF" stroke-width="6" stroke-linecap="round"/>
      <path d="M 155 140 L 155 175 L 80 175" fill="none" stroke="#00D2FF" stroke-width="6" stroke-linecap="round"/>
      <!-- Monstrous RTX 4090 GPU Block -->
      <rect x="40" y="180" width="260" height="70" rx="4" fill="#080B10" stroke="#00F298" stroke-width="2"/>
      <text x="170" y="222" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="800" fill="#00F298">NVIDIA RTX 4090 24GB</text>
      <!-- Bottom Dual Fans -->
      <circle cx="95" cy="285" r="20" fill="none" stroke="#334255" stroke-width="2"/>
      <circle cx="170" cy="285" r="20" fill="none" stroke="#334255" stroke-width="2"/>
      <circle cx="245" cy="285" r="20" fill="none" stroke="#334255" stroke-width="2"/>
    </g>`
  ),

  'proj-ghost.svg': wrapSvg(
    'Project Ghost // Pure Snow White 1440p Esports Rig',
    'Ryzen 7 7800X3D • RTX 4070 Super White • Lian Li O11 Mini Snow • 240+ FPS',
    `<!-- Snow White Rig Vector -->
    <g transform="translate(230, 80)">
      <!-- Snow White Case Perimeter -->
      <rect x="0" y="0" width="340" height="340" rx="10" fill="#141B26" stroke="#FFFFFF" stroke-width="2"/>
      <!-- Panoramic Glass Pane Area -->
      <rect x="25" y="25" width="290" height="290" fill="#0E141E" stroke="#4A5A72" stroke-width="1.5"/>
      <!-- White Deepcool AIO Pump -->
      <rect x="120" y="70" width="70" height="70" rx="35" fill="#182230" stroke="#00D2FF" stroke-width="2.5"/>
      <circle cx="155" cy="105" r="16" fill="none" stroke="#FFFFFF" stroke-width="2"/>
      <!-- White GPU Shroud -->
      <rect x="40" y="180" width="260" height="65" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5"/>
      <text x="170" y="220" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="800" fill="#0F172A">RTX 4070 SUPER WHITE</text>
      <!-- White Top Radiator Fans -->
      <circle cx="95" cy="45" r="15" fill="none" stroke="#00D2FF" stroke-width="1.5"/>
      <circle cx="170" cy="45" r="15" fill="none" stroke="#00D2FF" stroke-width="1.5"/>
      <circle cx="245" cy="45" r="15" fill="none" stroke="#00D2FF" stroke-width="1.5"/>
    </g>`
  ),

  'proj-valkyrie.svg': wrapSvg(
    'Project Valkyrie // $850 Sustainable Bang-For-Buck',
    'Open-Air Bent Steel Bench • Ryzen 5 7600 • RX 6700 XT 12GB • 100% Recycled',
    `<!-- Valkyrie Open Frame Vector -->
    <g transform="translate(230, 80)">
      <polygon points="20,330 320,330 340,300 40,300" fill="#202A38" stroke="#00F298" stroke-width="2"/>
      <rect x="50" y="30" width="240" height="270" rx="6" fill="#0C1017" stroke="#2E3C50" stroke-width="1.5"/>
      <!-- Exposed Heatsink Tower -->
      <rect x="110" y="60" width="80" height="90" fill="#18212D" stroke="#00F298" stroke-width="1.5"/>
      <line x1="110" y1="75" x2="190" y2="75" stroke="#485B74" stroke-width="2"/>
      <line x1="110" y1="95" x2="190" y2="95" stroke="#485B74" stroke-width="2"/>
      <line x1="110" y1="115" x2="190" y2="115" stroke="#485B74" stroke-width="2"/>
      <line x1="110" y1="135" x2="190" y2="135" stroke="#485B74" stroke-width="2"/>
      <!-- Vertical GPU Mount -->
      <rect x="70" y="180" width="200" height="60" rx="4" fill="#111620" stroke="#00D2FF" stroke-width="2"/>
      <text x="170" y="216" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#00D2FF">RX 6700 XT 12GB</text>
      <text x="170" y="270" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10" fill="#00F298">100% RECYCLED BENT STEEL</text>
    </g>`
  )
};

for (const [filename, content] of Object.entries(assets)) {
  const filePath = path.join(dir, filename);
  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`Generated: ${filename} (${content.length} bytes)`);
}

console.log('All 12 vector assets generated successfully!');
