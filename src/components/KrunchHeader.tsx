import React, { useState, useEffect } from 'react';
import { ShoppingBag, Volume2, VolumeX, Flame, Sparkles } from 'lucide-react';
import { KrunchLogo } from './KrunchLogo';
import { sfx } from './ReactiveButton';

interface KrunchHeaderProps {
  cartCount: number;
  onOpenCart: () => void;
  onScrollToSection: (id: string) => void;
}

export const KrunchHeader: React.FC<KrunchHeaderProps> = ({
  cartCount,
  onOpenCart,
  onScrollToSection,
}) => {
  const [sfxActive, setSfxActive] = useState<boolean>(true);
  const [griddleTemp, setGriddleTemp] = useState<number>(476);

  // Live griddle temperature simulation
  useEffect(() => {
    const timer = setInterval(() => {
      setGriddleTemp(475 + Math.floor(Math.random() * 4) - 2);
    }, 3500);
    return () => clearInterval(timer);
  }, []);

  const toggleSound = () => {
    const newState = !sfxActive;
    setSfxActive(newState);
    sfx.enabled = newState;
    if (newState) sfx.playCrunch();
  };

  return (
    <header className="sticky top-0 z-40 w-full bg-neutral-950/90 backdrop-blur-xl border-b border-neutral-800/80 transition-colors">
      
      {/* Topmost Telemetry Ticker Ribbon */}
      <div className="w-full bg-neutral-900 border-b border-neutral-800/60 py-1.5 px-4 font-mono text-[10px] sm:text-xs text-neutral-400 select-none overflow-x-auto">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5 text-lime-400 font-bold">
              <span className="w-2 h-2 rounded-full bg-lime-400 animate-ping" />
              FLAT-TOP LIVE // EAST AUSTIN ATELIER
            </span>
            <span className="hidden sm:inline text-neutral-600">|</span>
            <span className="hidden sm:inline">
              GRIDDLE: <strong className="text-amber-400 tabular-nums">{griddleTemp}°F SEAR</strong>
            </span>
            <span className="hidden md:inline text-neutral-600">|</span>
            <span className="hidden md:inline">
              BEEF: <strong>44 FARMS 40-DAY DRY AGED</strong>
            </span>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-neutral-500 hidden lg:inline">GEN Z × POP CULINARY WARFARE</span>
            <span className="px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 font-bold uppercase">
              DROPS ACTIVE
            </span>
          </div>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-8 h-20 flex items-center justify-between gap-4">
        
        {/* Brand Logo */}
        <div onClick={() => onScrollToSection('hero')}>
          <KrunchLogo size="md" />
        </div>

        {/* Center Nav Links */}
        <nav className="hidden lg:flex items-center gap-8 text-xs font-mono font-bold uppercase tracking-wider text-neutral-300">
          <button
            onClick={() => onScrollToSection('hero')}
            className="hover:text-amber-400 transition-colors flex items-center gap-1"
          >
            <span>3D BURGER</span>
            <span className="text-[9px] px-1 rounded bg-amber-500/20 text-amber-300">4K</span>
          </button>

          <button
            onClick={() => onScrollToSection('video-wall')}
            className="hover:text-amber-400 transition-colors flex items-center gap-1"
          >
            <span>CCTV STREAMS</span>
            <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
          </button>

          <button
            onClick={() => onScrollToSection('menu')}
            className="hover:text-amber-400 transition-colors"
          >
            POP CATERING MENU
          </button>

          <button
            onClick={() => onScrollToSection('sourcing')}
            className="hover:text-amber-400 transition-colors"
          >
            THE CULTURE & LORE
          </button>
        </nav>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          {/* SFX Haptic Toggle */}
          <button
            onClick={toggleSound}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-neutral-800 bg-neutral-900 text-xs font-mono text-neutral-300 hover:border-amber-400/60 transition-colors active:translate-y-[1px]"
            title="Toggle Procedural Bite Audio"
          >
            {sfxActive ? (
              <Volume2 className="w-3.5 h-3.5 text-amber-400" />
            ) : (
              <VolumeX className="w-3.5 h-3.5 text-neutral-500" />
            )}
            <span className="hidden sm:inline">SFX: {sfxActive ? 'ON' : 'OFF'}</span>
          </button>

          {/* Bite Bag Button */}
          <button
            onClick={onOpenCart}
            className="relative flex items-center gap-2.5 px-4 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-yellow-400 text-neutral-950 font-black text-xs uppercase tracking-wider hover:brightness-105 active:translate-y-[2px] transition-all shadow-lg shadow-amber-500/20 select-none"
          >
            <ShoppingBag className="w-4 h-4 stroke-[2.5]" />
            <span className="hidden sm:inline">BITE BAG</span>
            <span className="w-5 h-5 rounded-full bg-neutral-950 text-amber-400 flex items-center justify-center font-mono text-[11px] font-black tabular-nums">
              {cartCount}
            </span>
          </button>
        </div>

      </div>
    </header>
  );
};
