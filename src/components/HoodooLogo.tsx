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

interface HoodooLogoProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  palette?: BrandPalette;
}

export const HoodooLogo: React.FC<HoodooLogoProps> = ({
  className = '',
  size = 'md',
  palette = 'silver',
}) => {
  const heightClass =
    size === 'sm'
      ? 'h-8 sm:h-9'
      : size === 'lg'
      ? 'h-14 sm:h-16 md:h-20'
      : size === 'xl'
      ? 'h-20 sm:h-24 md:h-28'
      : 'h-11 sm:h-12 md:h-14';

  // CSS Linear Gradients matching brand palettes
  const gradients: Record<BrandPalette, string> = {
    silver: 'linear-gradient(135deg, #ffffff 0%, #e2e8f0 25%, #94a3b8 65%, #475569 100%)',
    cobalt: 'linear-gradient(135deg, #60a5fa 0%, #2563eb 50%, #1e40af 100%)',
    chrome: 'linear-gradient(135deg, #ffffff 0%, #f1f5f9 35%, #94a3b8 70%, #475569 100%)',
    cocoa: 'linear-gradient(135deg, #d7b9a5 0%, #9c6c4c 50%, #4a2c1f 100%)',
    crimson: 'linear-gradient(135deg, #f43f5e 0%, #be123c 50%, #4c0519 100%)',
    carbon: 'linear-gradient(135deg, #cbd5e1 0%, #64748b 50%, #0f172a 100%)',
  };

  const bgGradient = gradients[palette] || gradients.silver;

  return (
    <div className={`flex items-center select-none ${className}`}>
      <div
        className={`${heightClass} aspect-[883/398] transition-transform duration-200 hover:scale-[1.02] filter drop-shadow-[0_2px_8px_rgba(0,0,0,0.4)]`}
        style={{
          maskImage: 'url(/assets/hoodoo_logo.svg)',
          WebkitMaskImage: 'url(/assets/hoodoo_logo.svg)',
          maskSize: 'contain',
          WebkitMaskSize: 'contain',
          maskRepeat: 'no-repeat',
          WebkitMaskRepeat: 'no-repeat',
          maskPosition: 'center',
          WebkitMaskPosition: 'center',
          background: bgGradient,
        }}
        role="img"
        aria-label="HOODOO ATELIER"
      />
    </div>
  );
};
