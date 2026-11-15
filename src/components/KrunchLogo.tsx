import React from 'react';

interface KrunchLogoProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showSubtitle?: boolean;
}

export const KrunchLogo: React.FC<KrunchLogoProps> = ({
  className = '',
  size = 'md',
  showSubtitle = true,
}) => {
  const dimensions = {
    sm: 'h-10',
    md: 'h-14',
    lg: 'h-20',
    xl: 'h-28',
  }[size];

  return (
    <div className={`flex items-center gap-3 select-none group cursor-pointer ${className}`}>
      {/* 3D-Styled Stylized Chomping Mouth Graphic */}
      <div className={`relative ${dimensions} aspect-square flex-shrink-0 transition-transform duration-300 group-hover:scale-105 group-hover:rotate-[-3deg]`}>
        {/* Glow backdrop */}
        <div className="absolute inset-0 bg-gradient-to-tr from-amber-500/40 via-red-500/30 to-lime-400/40 rounded-full blur-md opacity-80 group-hover:opacity-100 transition-opacity" />
        
        {/* Raster Logo Thumbnail or Vector Mouth Graphic */}
        <div className="relative w-full h-full rounded-2xl bg-neutral-950 border-2 border-amber-400/80 p-1 overflow-hidden shadow-[0_0_20px_rgba(245,158,11,0.4)]">
          <img
            src="/assets/krunch_logo.jpg"
            alt="KRUNCHBIGMOUTHS Emblem"
            className="w-full h-full object-cover rounded-xl"
            onError={(e) => {
              // Fallback to SVG if image fails
              (e.currentTarget as HTMLElement).style.display = 'none';
            }}
          />
          {/* Overlay Bite Mark */}
          <div className="absolute -top-1 -right-1 w-4 h-4 bg-neutral-950 rounded-full border border-amber-400/50" />
        </div>
      </div>

      {/* Typography */}
      <div className="flex flex-col">
        <div className="flex items-center gap-1.5">
          <span className="font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-yellow-200 to-lime-400 font-sans text-xl sm:text-2xl lg:text-3xl leading-none drop-shadow-[0_2px_12px_rgba(245,158,11,0.5)]">
            KRUNCH
          </span>
          <span className="font-black tracking-tighter text-white font-sans text-xl sm:text-2xl lg:text-3xl leading-none drop-shadow-[0_2px_10px_rgba(255,255,255,0.3)]">
            BIGMOUTHS
          </span>
          <span className="px-1.5 py-0.5 rounded bg-lime-400 text-neutral-950 font-mono text-[9px] font-extrabold uppercase tracking-wider ml-1 rotate-3 animate-pulse">
            4K
          </span>
        </div>

        {showSubtitle && (
          <span className="font-mono text-[9px] sm:text-[10px] uppercase tracking-[0.22em] text-neutral-400 font-semibold mt-1">
            HYPER-DRIP BURGER SYNDICATE // AUSTIN × NIGHT CITY
          </span>
        )}
      </div>
    </div>
  );
};
