import React from 'react';
import { Moon, Sun, ShoppingBag, Move3d, Palette } from 'lucide-react';
import { HoodooLogo, BrandPalette, PALETTES } from './HoodooLogo';

interface HeaderProps {
  darkMode: boolean;
  setDarkMode: (val: boolean | ((prev: boolean) => boolean)) => void;
  cartCount: number;
  onOpenCart: () => void;
  currentPage: 'home' | 'about' | 'policy' | 'cookie-policy';
  onNavigate: (page: 'home' | 'about' | 'policy' | 'cookie-policy') => void;
  onOpen3D?: () => void;
  palette?: BrandPalette;
  onSelectPalette?: (palette: BrandPalette) => void;
}

export const Header: React.FC<HeaderProps> = ({
  darkMode,
  setDarkMode,
  cartCount,
  onOpenCart,
  currentPage,
  onNavigate,
  onOpen3D,
  palette = 'silver',
  onSelectPalette,
}) => {
  const currentPalette = PALETTES[palette] || PALETTES.silver;
  const paletteKeys: BrandPalette[] = ['silver', 'cobalt', 'chrome', 'cocoa', 'crimson', 'carbon'];

  return (
    <header className="sticky top-0 z-40 w-full bg-[#f5f5f4]/95 dark:bg-[#0a0a0c]/95 backdrop-blur-md transition-colors border-b border-neutral-200/60 dark:border-neutral-800/60">
      <div className="max-w-[1600px] mx-auto px-6 lg:px-12 h-20 sm:h-24 flex items-center justify-between">
        
        {/* Brand Logo: Clean Architectural HooDoo Vector Logo with Dynamic Palette */}
        <button
          onClick={() => onNavigate('home')}
          className="group flex items-center gap-3 transition-transform hover:opacity-95 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm"
          aria-label="HOODOO Home"
        >
          <HoodooLogo size="lg" palette={palette} />
        </button>

        {/* Navigation & Controls */}
        <div className="flex items-center gap-6 sm:gap-10">
          <nav className="flex items-center gap-6 sm:gap-8 text-xs sm:text-sm font-bold tracking-wider uppercase font-sans">
            <button
              onClick={() => onNavigate('home')}
              className={`transition-colors py-1 relative focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm ${
                currentPage === 'home'
                  ? 'text-neutral-950 dark:text-white font-extrabold'
                  : 'text-neutral-600 dark:text-neutral-300 hover:text-neutral-950 dark:hover:text-white'
              }`}
            >
              CATALOG
              {currentPage === 'home' && (
                <span className="absolute -bottom-1 left-0 right-0 h-[2px] bg-neutral-950 dark:bg-white rounded-full" />
              )}
            </button>

            <button
              onClick={() => onNavigate('about')}
              className={`transition-colors py-1 relative focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm ${
                currentPage === 'about'
                  ? 'text-neutral-950 dark:text-white font-extrabold'
                  : 'text-neutral-600 dark:text-neutral-300 hover:text-neutral-950 dark:hover:text-white'
              }`}
            >
              ABOUT US
              {currentPage === 'about' && (
                <span className="absolute -bottom-1 left-0 right-0 h-[2px] bg-neutral-950 dark:bg-white rounded-full" />
              )}
            </button>

            <button
              onClick={() => onNavigate('policy')}
              className={`transition-colors py-1 relative focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm ${
                currentPage === 'policy'
                  ? 'text-neutral-950 dark:text-white font-extrabold'
                  : 'text-neutral-600 dark:text-neutral-300 hover:text-neutral-950 dark:hover:text-white'
              }`}
            >
              POLICY
              {currentPage === 'policy' && (
                <span className="absolute -bottom-1 left-0 right-0 h-[2px] bg-neutral-950 dark:bg-white rounded-full" />
              )}
            </button>

            {onOpen3D && (
              <button
                onClick={onOpen3D}
                className={`flex items-center gap-1.5 px-3 py-1 text-xs font-mono font-bold tracking-wider rounded-full ${currentPalette.buttonClass} shadow-sm transition-all active:scale-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400`}
                aria-label="Open 3D Studio"
              >
                <Move3d className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">3D STUDIO</span>
              </button>
            )}
          </nav>

          {/* Palette Selector Bar */}
          {onSelectPalette && (
            <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-neutral-200/50 dark:bg-neutral-800/50 border border-neutral-300/40 dark:border-neutral-700/40">
              <Palette className="w-3.5 h-3.5 text-neutral-500 mr-0.5" />
              {paletteKeys.map((pKey) => {
                const conf = PALETTES[pKey];
                const isSelected = palette === pKey;
                return (
                  <button
                    key={pKey}
                    onClick={() => onSelectPalette(pKey)}
                    title={`Palette: ${conf.name}`}
                    className={`w-4 h-4 rounded-full transition-all flex items-center justify-center ${
                      isSelected
                        ? 'ring-2 ring-neutral-900 dark:ring-white scale-110'
                        : 'opacity-70 hover:opacity-100 hover:scale-105'
                    }`}
                    style={{ backgroundColor: conf.primary }}
                    aria-label={`Select ${conf.name} palette`}
                  >
                    {isSelected && (
                      <span className="w-1 h-1 rounded-full bg-white dark:bg-neutral-950" />
                    )}
                  </button>
                );
              })}
            </div>
          )}

          {/* Theme Toggle & Bag */}
          <div className="flex items-center gap-3 sm:gap-5">
            <button
              onClick={() => setDarkMode((prev) => !prev)}
              aria-label="Toggle Theme"
              className="p-2 text-neutral-600 dark:text-neutral-300 hover:text-neutral-950 dark:hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm"
            >
              {darkMode ? (
                <Sun className="w-5 h-5 transition-transform hover:rotate-45" />
              ) : (
                <Moon className="w-5 h-5 transition-transform hover:-rotate-12 fill-neutral-700" />
              )}
            </button>

            <button
              onClick={onOpenCart}
              aria-label="Open Shopping Bag"
              className="relative p-2 text-neutral-950 dark:text-white hover:opacity-80 transition-opacity focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm"
            >
              <ShoppingBag className="w-5 h-5 stroke-[2]" />
              {cartCount > 0 && (
                <span className="absolute -top-1 -right-2 min-w-[18px] h-[18px] px-1 bg-neutral-950 text-white dark:bg-white dark:text-black text-[10px] font-extrabold rounded-full flex items-center justify-center">
                  {cartCount}
                </span>
              )}
            </button>
          </div>
        </div>

      </div>
    </header>
  );
};
