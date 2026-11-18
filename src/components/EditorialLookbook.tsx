import React, { useState } from 'react';
import { Camera, Maximize2, Shield, Eye } from 'lucide-react';

interface LookbookItem {
  id: string;
  title: string;
  subtitle: string;
  category: string;
  image: string;
  alt: string;
  coordinates: string;
  focal: string;
  specs: string[];
}

const LOOKBOOK_ITEMS: LookbookItem[] = [
  {
    id: 'lb-1',
    title: 'THE CONCRETE DOCTRINE',
    subtitle: '500GSM Brutal-weight Fleece Drape',
    category: 'CAMPAIGN 01',
    image: '/assets/editorial_graded/streetwear_hoodie_model.webp',
    alt: 'High-fashion editorial of heavyweight black hoodie silhouette in brutalist urban environment',
    coordinates: '34°03\'12"N 118°14\'35"W',
    focal: '50mm f/1.4 • 1/500s',
    specs: ['500GSM Iron Fleece', 'Drop Shoulder Boxy Cut', 'Double-needle Hem']
  },
  {
    id: 'lb-2',
    title: 'RAW COMBED TEXTILE WEAVE',
    subtitle: 'High-Density 100% Cotton Macro Geometry',
    category: 'MATERIAL SPEC',
    image: '/assets/editorial_graded/heavy_textile_macro.webp',
    alt: 'Extreme close-up macro texture of heavy combed cotton textile weave',
    coordinates: 'LOS ANGELES ATELIER',
    focal: '90mm Macro f/2.8',
    specs: ['Zero Polyester Blend', 'Discharge Ink Penetration', 'Pre-shrunk Vintage Hand']
  },
  {
    id: 'lb-3',
    title: 'VULCANIZED SOLE FRICTION',
    subtitle: 'Skate-Tuned Dual Density Rubber',
    category: 'FOOTWEAR ARCHIVE',
    image: '/assets/editorial_graded/skate_concrete_curb.webp',
    alt: 'Editorial street shot of skate curb friction and footwear geometry',
    coordinates: 'VENICE CONCRETE PIT',
    focal: '35mm f/2.0 • Tri-X 400',
    specs: ['Cupsole Architecture', 'Reinforced Padded Collar', 'Ballistic Suede Uppers']
  },
  {
    id: 'lb-4',
    title: 'ARCHITECTURAL PROPORTIONS',
    subtitle: 'Stiff Unforgiving Silhouette on Concrete',
    category: 'DRAPE STUDY',
    image: '/assets/editorial_graded/oversized_streetwear_editorial.webp',
    alt: 'Full-length streetwear silhouette showing stiff heavyweight drape and proportions',
    coordinates: 'DOWNTOWN INDUSTRIAL DISTRICT',
    focal: '85mm f/1.8 • Kodak 5219',
    specs: ['Architectural Drape', 'No Sagging Lines', 'Brushed Metal Hardware']
  }
];

export const EditorialLookbook: React.FC = () => {
  const [activeModalItem, setActiveModalItem] = useState<LookbookItem | null>(null);

  return (
    <section 
      className="w-full max-w-[1600px] mx-auto px-6 lg:px-12 py-16 lg:py-24 border-t border-neutral-200/80 dark:border-neutral-800/80"
      aria-label="Editorial Lookbook Archive"
    >
      {/* Section Header */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-10">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-[11px] font-mono font-bold tracking-widest text-neutral-600 dark:text-neutral-400 uppercase">
              EDITORIAL ARCHIVE • SHOT ON 35MM
            </span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black uppercase tracking-tight text-neutral-950 dark:text-white font-display">
            THE CONCRETE DOCTRINE
          </h2>
          <p className="mt-2 text-xs sm:text-sm text-neutral-600 dark:text-neutral-400 max-w-xl font-sans">
            Visual studies of weight, drape, and street architecture documented across Los Angeles. Real garments, zero synthetic filters.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs font-mono font-semibold px-3 py-1 rounded-full bg-neutral-200/70 dark:bg-neutral-800/70 text-neutral-700 dark:text-neutral-300 border border-neutral-300/60 dark:border-neutral-700/60">
            AUTUMN/WINTER LOOKBOOK
          </span>
        </div>
      </div>

      {/* Editorial Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-stretch">
        
        {/* Card 1: Large Featured Vertical Editorial */}
        <article className="md:col-span-12 lg:col-span-6 group relative rounded-2xl overflow-hidden bg-neutral-900 border border-neutral-200/60 dark:border-neutral-800/80 min-h-[480px] lg:min-h-[580px] flex flex-col justify-end p-6 sm:p-8">
          <img
            src={LOOKBOOK_ITEMS[0].image}
            alt={LOOKBOOK_ITEMS[0].alt}
            loading="lazy"
            decoding="async"
            className="absolute inset-0 w-full h-full object-cover object-top filter grayscale contrast-125 transition-transform duration-700 ease-out group-hover:scale-105 opacity-80 group-hover:opacity-90"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-neutral-950/40 to-transparent" />
          
          {/* Top Metadata Badges */}
          <div className="absolute top-4 left-4 right-4 flex items-center justify-between z-10">
            <span className="text-[10px] font-mono font-extrabold uppercase tracking-widest px-2.5 py-1 rounded-full bg-neutral-950/80 text-white backdrop-blur-md border border-neutral-700/60">
              {LOOKBOOK_ITEMS[0].category}
            </span>
            <span className="text-[10px] font-mono tracking-widest text-neutral-300 bg-neutral-950/80 px-2 py-0.5 rounded backdrop-blur-md border border-neutral-800">
              {LOOKBOOK_ITEMS[0].coordinates}
            </span>
          </div>

          {/* Bottom Caption & Specs */}
          <div className="relative z-10 space-y-3">
            <h3 className="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white font-display">
              {LOOKBOOK_ITEMS[0].title}
            </h3>
            <p className="text-xs sm:text-sm text-neutral-300 font-sans max-w-md">
              {LOOKBOOK_ITEMS[0].subtitle}
            </p>
            <div className="flex flex-wrap gap-2 pt-2">
              {LOOKBOOK_ITEMS[0].specs.map((spec, i) => (
                <span
                  key={i}
                  className="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded bg-neutral-900/90 text-neutral-200 border border-neutral-700/80"
                >
                  {spec}
                </span>
              ))}
            </div>
          </div>
        </article>

        {/* Right Column: 3 Editorial Tiles */}
        <div className="md:col-span-12 lg:col-span-6 grid grid-cols-1 sm:grid-cols-2 gap-6">
          
          {/* Card 2: Material Spec */}
          <article className="group relative rounded-2xl overflow-hidden bg-neutral-900 border border-neutral-200/60 dark:border-neutral-800/80 min-h-[280px] flex flex-col justify-end p-5">
            <img
              src={LOOKBOOK_ITEMS[1].image}
              alt={LOOKBOOK_ITEMS[1].alt}
              loading="lazy"
              decoding="async"
              className="absolute inset-0 w-full h-full object-cover filter grayscale contrast-125 transition-transform duration-700 ease-out group-hover:scale-105 opacity-75 group-hover:opacity-85"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-neutral-950/50 to-transparent" />
            
            <div className="absolute top-3 left-3 z-10">
              <span className="text-[10px] font-mono font-bold uppercase tracking-widest px-2 py-0.5 rounded bg-neutral-950/80 text-white backdrop-blur-md border border-neutral-700/60">
                {LOOKBOOK_ITEMS[1].category}
              </span>
            </div>

            <div className="relative z-10 space-y-1.5">
              <h3 className="text-lg font-black uppercase tracking-tight text-white font-display">
                {LOOKBOOK_ITEMS[1].title}
              </h3>
              <p className="text-[11px] text-neutral-300 font-sans">
                {LOOKBOOK_ITEMS[1].subtitle}
              </p>
              <div className="pt-1">
                <span className="text-[9px] font-mono uppercase text-neutral-400">
                  {LOOKBOOK_ITEMS[1].focal}
                </span>
              </div>
            </div>
          </article>

          {/* Card 3: Footwear Detail */}
          <article className="group relative rounded-2xl overflow-hidden bg-neutral-900 border border-neutral-200/60 dark:border-neutral-800/80 min-h-[280px] flex flex-col justify-end p-5">
            <img
              src={LOOKBOOK_ITEMS[2].image}
              alt={LOOKBOOK_ITEMS[2].alt}
              loading="lazy"
              decoding="async"
              className="absolute inset-0 w-full h-full object-cover filter grayscale contrast-125 transition-transform duration-700 ease-out group-hover:scale-105 opacity-75 group-hover:opacity-85"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-neutral-950/50 to-transparent" />
            
            <div className="absolute top-3 left-3 z-10">
              <span className="text-[10px] font-mono font-bold uppercase tracking-widest px-2 py-0.5 rounded bg-neutral-950/80 text-white backdrop-blur-md border border-neutral-700/60">
                {LOOKBOOK_ITEMS[2].category}
              </span>
            </div>

            <div className="relative z-10 space-y-1.5">
              <h3 className="text-lg font-black uppercase tracking-tight text-white font-display">
                {LOOKBOOK_ITEMS[2].title}
              </h3>
              <p className="text-[11px] text-neutral-300 font-sans">
                {LOOKBOOK_ITEMS[2].subtitle}
              </p>
              <div className="pt-1">
                <span className="text-[9px] font-mono uppercase text-neutral-400">
                  {LOOKBOOK_ITEMS[2].focal}
                </span>
              </div>
            </div>
          </article>

          {/* Card 4: Full Wide Span Card */}
          <article className="sm:col-span-2 group relative rounded-2xl overflow-hidden bg-neutral-900 border border-neutral-200/60 dark:border-neutral-800/80 min-h-[260px] flex flex-col justify-end p-6">
            <img
              src={LOOKBOOK_ITEMS[3].image}
              alt={LOOKBOOK_ITEMS[3].alt}
              loading="lazy"
              decoding="async"
              className="absolute inset-0 w-full h-full object-cover object-center filter grayscale contrast-125 transition-transform duration-700 ease-out group-hover:scale-105 opacity-75 group-hover:opacity-85"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-neutral-950/60 to-transparent" />
            
            <div className="absolute top-3 left-3 z-10">
              <span className="text-[10px] font-mono font-bold uppercase tracking-widest px-2 py-0.5 rounded bg-neutral-950/80 text-white backdrop-blur-md border border-neutral-700/60">
                {LOOKBOOK_ITEMS[3].category}
              </span>
            </div>

            <div className="relative z-10 flex flex-col sm:flex-row sm:items-end justify-between gap-3">
              <div className="space-y-1">
                <h3 className="text-xl font-black uppercase tracking-tight text-white font-display">
                  {LOOKBOOK_ITEMS[3].title}
                </h3>
                <p className="text-xs text-neutral-300 font-sans">
                  {LOOKBOOK_ITEMS[3].subtitle}
                </p>
              </div>
              <div className="flex gap-2">
                <span className="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded bg-neutral-900/90 text-neutral-200 border border-neutral-700">
                  {LOOKBOOK_ITEMS[3].coordinates}
                </span>
              </div>
            </div>
          </article>

        </div>

      </div>
    </section>
  );
};
