import React from 'react';

export type BrandPalette = 'silver' | 'cobalt' | 'chrome' | 'cocoa' | 'crimson' | 'carbon';

export interface PaletteConfig {
  id: BrandPalette;
  name: string;
  primary: string;
  secondary: string;
  accent: string;
  glow: string;
  badgeBg: string;
  badgeText: string;
  ringClass: string;
  focusRing: string;
  buttonClass: string;
  activeFilterClass: string;
  pillTagClass: string;
  subtleClass: string;
  studioAccentClass: string;
}

export const PALETTES: Record<BrandPalette, PaletteConfig> = {
  silver: {
    id: 'silver',
    name: 'Brushed Silver',
    primary: '#cbd5e1',
    secondary: '#94a3b8',
    accent: '#f8fafc',
    glow: 'rgba(203, 213, 225, 0.35)',
    badgeBg: 'bg-neutral-900 text-neutral-100 dark:bg-white dark:text-neutral-950 border border-neutral-700/60 dark:border-neutral-300',
    badgeText: 'text-neutral-900 dark:text-neutral-100 font-bold',
    ringClass: 'ring-neutral-400 dark:ring-neutral-200',
    focusRing: 'focus-visible:ring-neutral-400',
    buttonClass: 'bg-neutral-900 hover:bg-neutral-800 text-white dark:bg-neutral-100 dark:text-neutral-950 dark:hover:bg-white shadow-sm border border-neutral-700/50 dark:border-neutral-300/80',
    activeFilterClass: 'bg-neutral-900 text-white border-neutral-900 dark:bg-white dark:text-neutral-950 dark:border-white shadow-sm',
    pillTagClass: 'bg-neutral-900 hover:bg-neutral-800 text-white dark:bg-white dark:text-neutral-950',
    subtleClass: 'bg-neutral-200/80 text-neutral-900 dark:bg-neutral-800/80 dark:text-neutral-100 border border-neutral-300/80 dark:border-neutral-700/80',
    studioAccentClass: 'text-neutral-100 bg-neutral-850/80 border-neutral-600/60 shadow-lg',
  },
  cobalt: {
    id: 'cobalt',
    name: 'Royal Cobalt',
    primary: '#1d4ed8',
    secondary: '#1e40af',
    accent: '#3b82f6',
    glow: 'rgba(29, 78, 216, 0.25)',
    badgeBg: 'bg-blue-700',
    badgeText: 'text-blue-700 dark:text-blue-400',
    ringClass: 'ring-blue-700',
    focusRing: 'focus-visible:ring-blue-600',
    buttonClass: 'bg-blue-700 hover:bg-blue-800 text-white',
    activeFilterClass: 'bg-blue-700 text-white border-blue-700 dark:bg-blue-600 dark:border-blue-600',
    pillTagClass: 'bg-blue-700 hover:bg-blue-800 text-white',
    subtleClass: 'bg-blue-900/10 text-blue-800 dark:bg-blue-950/40 dark:text-blue-300',
    studioAccentClass: 'text-blue-300 bg-blue-950/40 border-blue-800/40',
  },
  chrome: {
    id: 'chrome',
    name: 'Liquid Chrome',
    primary: '#64748b',
    secondary: '#475569',
    accent: '#94a3b8',
    glow: 'rgba(148, 163, 184, 0.2)',
    badgeBg: 'bg-neutral-900 dark:bg-white',
    badgeText: 'text-neutral-900 dark:text-white',
    ringClass: 'ring-neutral-400',
    focusRing: 'focus-visible:ring-neutral-400',
    buttonClass: 'bg-neutral-950 hover:bg-neutral-800 text-white dark:bg-white dark:text-black dark:hover:bg-neutral-200',
    activeFilterClass: 'bg-neutral-950 text-white border-neutral-950 dark:bg-white dark:text-neutral-950 dark:border-white',
    pillTagClass: 'bg-neutral-900 hover:bg-neutral-800 text-white dark:bg-white dark:text-neutral-950',
    subtleClass: 'bg-neutral-300/40 text-neutral-800 dark:bg-neutral-800/60 dark:text-neutral-200',
    studioAccentClass: 'text-slate-300 bg-slate-800/40 border-slate-700/40',
  },
  cocoa: {
    id: 'cocoa',
    name: 'Washed Cocoa',
    primary: '#5c4033',
    secondary: '#3d2b24',
    accent: '#8c6d58',
    glow: 'rgba(92, 64, 51, 0.25)',
    badgeBg: 'bg-[#5c4033]',
    badgeText: 'text-[#5c4033] dark:text-[#c4a482]',
    ringClass: 'ring-[#5c4033]',
    focusRing: 'focus-visible:ring-[#5c4033]',
    buttonClass: 'bg-[#5c4033] hover:bg-[#4a3328] text-white',
    activeFilterClass: 'bg-[#5c4033] text-white border-[#5c4033] dark:bg-[#4a3328] dark:border-[#4a3328]',
    pillTagClass: 'bg-[#5c4033] hover:bg-[#4a3328] text-white',
    subtleClass: 'bg-[#5c4033]/15 text-[#5c4033] dark:bg-[#5c4033]/30 dark:text-[#d7bea8]',
    studioAccentClass: 'text-[#d7bea8] bg-[#3d2b24]/50 border-[#5c4033]/40',
  },
  crimson: {
    id: 'crimson',
    name: 'Oxblood Noir',
    primary: '#881337',
    secondary: '#4c0519',
    accent: '#be123c',
    glow: 'rgba(136, 19, 55, 0.25)',
    badgeBg: 'bg-rose-900',
    badgeText: 'text-rose-900 dark:text-rose-300',
    ringClass: 'ring-rose-800',
    focusRing: 'focus-visible:ring-rose-700',
    buttonClass: 'bg-rose-900 hover:bg-rose-950 text-white',
    activeFilterClass: 'bg-rose-900 text-white border-rose-900 dark:bg-rose-800 dark:border-rose-800',
    pillTagClass: 'bg-rose-900 hover:bg-rose-950 text-white',
    subtleClass: 'bg-rose-900/10 text-rose-900 dark:bg-rose-950/40 dark:text-rose-300',
    studioAccentClass: 'text-rose-300 bg-rose-950/50 border-rose-800/40',
  },
  carbon: {
    id: 'carbon',
    name: 'Stealth Carbon',
    primary: '#334155',
    secondary: '#1e293b',
    accent: '#475569',
    glow: 'rgba(51, 65, 85, 0.25)',
    badgeBg: 'bg-slate-800',
    badgeText: 'text-slate-700 dark:text-slate-300',
    ringClass: 'ring-slate-600',
    focusRing: 'focus-visible:ring-slate-500',
    buttonClass: 'bg-slate-800 hover:bg-slate-900 text-white',
    activeFilterClass: 'bg-slate-800 text-white border-slate-800 dark:bg-slate-700 dark:border-slate-700',
    pillTagClass: 'bg-slate-800 hover:bg-slate-900 text-white',
    subtleClass: 'bg-slate-600/10 text-slate-700 dark:bg-slate-800/40 dark:text-slate-300',
    studioAccentClass: 'text-slate-300 bg-slate-900/60 border-slate-700/40',
  },
};

const LOGO_PATH = "M 47 2.5 L 76.5 2 L 105.5 11 L 125.5 13 L 130.5 11 L 138.5 11 L 162.5 2 L 167.5 3 L 175.5 2 L 179 5.5 L 180 15.5 L 181.5 17 L 184.5 17 L 189.5 14 L 222.5 2 L 236.5 2 L 239 3.5 L 241 7.5 L 241 17.5 L 247 26.5 L 244.5 29 L 241.5 29 L 215.5 41 L 199 55.5 L 193 67.5 L 191 82.5 L 191 99.5 L 194.5 100 L 244.5 62 L 260.5 61 L 283.5 77 L 299 92.5 L 306 102.5 L 310 110.5 L 313 123.5 L 316 128.5 L 319 139.5 L 320 164.5 L 321 165.5 L 321 210.5 L 320 211.5 L 319 232.5 L 312 249.5 L 303 261.5 L 289.5 275 L 244 312.5 L 245.5 315 L 251.5 316 L 256 320.5 L 256 330.5 L 262 339.5 L 262 346.5 L 256.5 353 L 249.5 356 L 239.5 356 L 229.5 350 L 220.5 350 L 212.5 345 L 205 333.5 L 205 309.5 L 202.5 307 L 188.5 302 L 183.5 302 L 178.5 299 L 174.5 299 L 168.5 296 L 134.5 290 L 107.5 290 L 87.5 293 L 64.5 302 L 55 310.5 L 52 316.5 L 53 324.5 L 58 333.5 L 59 340.5 L 58 344.5 L 51.5 350 L 47.5 350 L 38.5 344 L 28.5 344 L 21 337.5 L 18 329.5 L 18 310.5 L 21 299.5 L 31 284.5 L 60 253.5 L 70 235.5 L 68.5 233 L 66.5 233 L 56.5 245 L 50.5 244 L 44.5 239 L 34.5 239 L 31 236.5 L 31 219.5 L 34 209.5 L 40 200.5 L 47.5 194 L 53.5 191 L 62.5 188 L 67.5 188 L 69 186.5 L 66 174.5 L 58.5 165 L 49.5 164 L 42.5 167 L 38 170.5 L 28.5 185 L 24.5 184 L 18.5 179 L 7.5 179 L 5 176.5 L 4 172.5 L 4 162.5 L 7 151.5 L 10 144.5 L 18.5 134 L 26.5 128 L 40.5 122 L 62.5 122 L 65 120.5 L 65 105.5 L 67 97.5 L 67 89.5 L 73 72.5 L 79 61.5 L 82 58.5 L 81.5 54 L 68.5 53 L 55.5 50 L 46.5 50 L 40.5 53 L 37 56.5 L 33 63.5 L 31 68.5 L 31 73.5 L 28.5 77 L 21.5 77 L 14.5 71 L 3.5 71 L 2 69.5 L 2 54.5 L 4 45.5 L 7 39.5 L 7 36.5 L 13 26.5 L 28.5 11 L 38.5 5 L 47 2.5 Z M 680 18.5 L 691.5 19 L 693.5 18 L 697.5 20 L 810.5 99 L 813.5 99 L 816.5 95 L 824.5 90 L 838.5 90 L 840 92.5 L 840 100.5 L 842 105.5 L 845 108.5 L 845 116.5 L 841 123.5 L 839 133.5 L 839 273.5 L 832.5 278 L 822.5 281 L 801.5 291 L 779.5 307 L 775.5 307 L 768.5 302 L 762.5 301 L 758.5 302 L 747.5 294 L 725.5 282 L 713.5 280 L 702.5 281 L 695.5 275 L 683.5 275 L 682 273.5 L 682 255.5 L 691 242.5 L 692 233.5 L 692 128.5 L 693 127.5 L 693 117.5 L 695.5 115 L 706.5 112 L 708.5 110 L 711.5 110 L 720 105.5 L 717.5 102 L 684.5 80 L 679 73.5 L 679 20.5 L 680 18.5 Z M 135.5 63 L 130 70.5 L 124 96.5 L 124.5 213 L 127 211.5 L 130 205.5 L 133 192.5 L 133 83.5 L 136 71.5 L 135.5 63 Z M 406 86.5 L 416.5 87 L 418.5 86 L 443.5 101 L 462.5 109 L 468.5 110 L 474.5 113 L 478.5 113 L 484.5 116 L 486 118.5 L 487 129.5 L 491 135.5 L 491 273.5 L 485.5 278 L 462.5 287 L 449.5 294 L 432.5 307 L 429.5 307 L 421.5 302 L 417.5 301 L 412.5 302 L 376.5 281 L 369.5 280 L 355.5 281 L 347.5 275 L 336.5 275 L 335 273.5 L 336 271.5 L 335 260.5 L 342 251.5 L 346 239.5 L 346 120.5 L 351.5 116 L 362.5 113 L 380.5 104 L 383.5 101 L 394.5 95 L 403.5 87 L 406 86.5 Z M 580 86.5 L 590.5 87 L 592.5 86 L 617.5 101 L 636.5 109 L 642.5 110 L 648.5 113 L 652.5 113 L 658.5 116 L 660 118.5 L 661 129.5 L 665 135.5 L 665 273.5 L 659.5 278 L 636.5 287 L 623.5 294 L 606.5 307 L 603.5 307 L 595.5 302 L 591.5 301 L 586.5 302 L 550.5 281 L 543.5 280 L 529.5 281 L 521.5 275 L 510.5 275 L 509 273.5 L 510 271.5 L 509 260.5 L 516 251.5 L 520 239.5 L 520 120.5 L 525.5 116 L 536.5 113 L 554.5 104 L 557.5 101 L 568.5 95 L 577.5 87 L 580 86.5 Z M 928 86.5 L 938.5 87 L 940.5 86 L 965.5 101 L 984.5 109 L 990.5 110 L 996.5 113 L 1000.5 113 L 1006.5 116 L 1008 118.5 L 1009 129.5 L 1013 135.5 L 1013 273.5 L 1007.5 278 L 984.5 287 L 971.5 294 L 954.5 307 L 951.5 307 L 943.5 302 L 939.5 301 L 934.5 302 L 898.5 281 L 891.5 280 L 877.5 281 L 869.5 275 L 858.5 275 L 857 273.5 L 858 271.5 L 857 260.5 L 864 251.5 L 868 239.5 L 868 120.5 L 873.5 116 L 884.5 113 L 902.5 104 L 905.5 101 L 916.5 95 L 925.5 87 L 928 86.5 Z M 1102 86.5 L 1112.5 87 L 1114.5 86 L 1139.5 101 L 1158.5 109 L 1164.5 110 L 1170.5 113 L 1174.5 113 L 1180.5 116 L 1182 118.5 L 1183 129.5 L 1187 135.5 L 1187 273.5 L 1181.5 278 L 1158.5 287 L 1145.5 294 L 1128.5 307 L 1125.5 307 L 1117.5 302 L 1113.5 301 L 1108.5 302 L 1072.5 281 L 1065.5 280 L 1051.5 281 L 1043.5 275 L 1032.5 275 L 1031 273.5 L 1032 271.5 L 1031 260.5 L 1038 251.5 L 1042 239.5 L 1042 120.5 L 1047.5 116 L 1058.5 113 L 1076.5 104 L 1079.5 101 L 1090.5 95 L 1099.5 87 L 1102 86.5 Z M 236.5 110 L 201.5 135 L 199 137.5 L 199 139.5 L 208.5 143 L 215.5 143 L 220.5 145 L 233.5 145 L 237.5 143 L 243.5 143 L 257.5 137 L 259 135.5 L 259 132.5 L 253 123.5 L 243.5 114 L 236.5 110 Z M 754.5 131 L 751 134.5 L 751 240.5 L 772.5 251 L 780.5 253 L 781 147.5 L 760.5 132 L 754.5 131 Z M 403.5 135 L 403 240.5 L 410.5 245 L 420.5 248 L 429.5 253 L 432.5 253 L 433 149.5 L 430.5 147 L 410.5 137 L 403.5 135 Z M 577.5 135 L 577 240.5 L 584.5 245 L 594.5 248 L 603.5 253 L 606.5 253 L 607 149.5 L 604.5 147 L 584.5 137 L 577.5 135 Z M 925.5 135 L 925 240.5 L 932.5 245 L 942.5 248 L 951.5 253 L 954.5 253 L 955 149.5 L 952.5 147 L 932.5 137 L 925.5 135 Z M 1099.5 135 L 1099 240.5 L 1106.5 245 L 1116.5 248 L 1125.5 253 L 1128.5 253 L 1129 149.5 L 1126.5 147 L 1106.5 137 L 1099.5 135 Z M 192.5 164 L 191 165.5 L 191 183.5 L 192.5 185 L 197.5 185 L 205.5 182 L 243.5 182 L 256.5 185 L 258.5 187 L 261.5 187 L 263 184.5 L 262 176.5 L 263 172.5 L 261.5 170 L 247.5 173 L 226.5 173 L 212.5 170 L 205.5 167 L 201.5 167 L 196.5 164 L 192.5 164 Z M 229.5 209 L 212.5 212 L 188.5 221 L 179.5 227 L 177.5 227 L 159 240.5 L 161.5 242 L 181.5 242 L 187.5 244 L 197.5 244 L 209.5 239 L 220.5 228 L 223.5 229 L 234.5 228 L 241 233.5 L 240 236.5 L 241 245.5 L 243.5 248 L 245.5 248 L 249 244.5 L 256 232.5 L 261 219.5 L 261 214.5 L 257.5 212 L 253.5 212 L 245.5 209 L 229.5 209 Z";

interface HoodooLogoProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  palette?: BrandPalette;
  showSubtitle?: boolean;
}

export const HoodooLogo: React.FC<HoodooLogoProps> = ({
  className = '',
  size = 'md',
  palette = 'silver',
  showSubtitle = true,
}) => {
  const heightClass =
    size === 'sm'
      ? 'h-6 sm:h-7'
      : size === 'lg'
      ? 'h-11 sm:h-13'
      : size === 'xl'
      ? 'h-16 sm:h-20'
      : 'h-8 sm:h-9';

  // Metallic gradient definitions for SVG fill
  const gradientStops: Record<BrandPalette, { c1: string; c2: string; c3: string }> = {
    silver: { c1: '#ffffff', c2: '#cbd5e1', c3: '#94a3b8' },
    cobalt: { c1: '#93c5fd', c2: '#3b82f6', c3: '#1d4ed8' },
    chrome: { c1: '#ffffff', c2: '#f1f5f9', c3: '#64748b' },
    cocoa: { c1: '#e2d4c9', c2: '#a8836a', c3: '#5c4033' },
    crimson: { c1: '#fda4af', c2: '#e11d48', c3: '#881337' },
    carbon: { c1: '#e2e8f0', c2: '#94a3b8', c3: '#475569' },
  };

  const currentGrad = gradientStops[palette] || gradientStops.silver;
  const gradId = `hoodoo-grad-${palette}`;

  return (
    <div className={`flex flex-col items-start select-none group ${className}`}>
      {/* SVG Wordmark with Authentic West Coast Gothic Calligraphy */}
      <svg
        viewBox="0 0 1189 358"
        className={`${heightClass} w-auto transition-transform duration-300 group-hover:scale-[1.03] filter drop-shadow-[0_2px_12px_rgba(0,0,0,0.5)]`}
        fill="currentColor"
        fillRule="evenodd"
        role="img"
        aria-label="HOODOO"
      >
        <defs>
          <linearGradient id={gradId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={currentGrad.c1} />
            <stop offset="45%" stopColor={currentGrad.c2} />
            <stop offset="100%" stopColor={currentGrad.c3} />
          </linearGradient>
        </defs>
        <path d={LOGO_PATH} fill={`url(#${gradId})`} />
      </svg>

      {/* Street Atelier Subtitle */}
      {showSubtitle && size !== 'sm' && (
        <div className="flex items-center gap-1.5 mt-0.5 pl-0.5 tracking-[0.28em] font-mono text-[8px] sm:text-[9px] font-bold text-neutral-400 group-hover:text-white transition-colors uppercase">
          <span>LOS ANGELES</span>
          <span className="text-neutral-600 dark:text-neutral-500">•</span>
          <span>ATELIER</span>
        </div>
      )}
    </div>
  );
};
