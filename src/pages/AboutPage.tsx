import React from 'react';
import { ArrowLeft } from 'lucide-react';

interface AboutPageProps {
  onBackToCatalog: () => void;
}

export const AboutPage: React.FC<AboutPageProps> = ({ onBackToCatalog }) => {
  return (
    <div className="max-w-[1200px] mx-auto px-6 lg:px-12 py-12 lg:py-20 animate-fadeIn">
      {/* Return to Catalog */}
      <button
        onClick={onBackToCatalog}
        className="inline-flex items-center gap-2 text-xs font-bold tracking-wider text-neutral-500 hover:text-neutral-950 dark:hover:text-white uppercase transition-colors mb-12"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>BACK TO CATALOG</span>
      </button>

      {/* Main Editorial Hero */}
      <div className="space-y-6 max-w-3xl mb-16">
        <span className="text-xs font-extrabold tracking-widest text-neutral-400 uppercase font-mono">
          BORN IN LOS ANGELES • WEST COAST LORE
        </span>
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black uppercase tracking-tight font-display text-neutral-950 dark:text-white leading-[1.05]">
          BUILT FOR THE STREETS. ZERO FAST-FASHION BS.
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-300 font-serif italic">
          "If your hoodie collapses after three washes, it wasn\'t made for the concrete."
        </p>
      </div>

      {/* Narrative Section */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-12 lg:gap-16 pt-8 border-t border-neutral-200/60 dark:border-neutral-800/60">
        
        <div className="md:col-span-5 space-y-4">
          <h2 className="text-xl font-black uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
            THE HOODOO DOCTRINE
          </h2>
          <p className="text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed">
            HOODOO was forged between Sunday lowrider hops down Whittier Boulevard and raw Venice skate pits. We were sick of corporate labels selling see-through poly-blend blanks with lazy graphics for $200.
          </p>
        </div>

        <div className="md:col-span-7 space-y-8 text-neutral-700 dark:text-neutral-300 text-sm sm:text-base leading-relaxed">
          <p>
            We mill our blanks at <strong>480GSM to 500GSM</strong>—thick enough to break the wind on a midnight freeway run and stiff enough to hold a true boxy street drape. No synthetic stretch. Just pure combed cotton that takes beatings, grease stains, and concrete scuffs, looking harder with every passing year.
          </p>
          <p>
            Our graphics pull straight from West Coast culture: hand-drawn Chicano blackletter calligraphy, lowrider hood pinstriping, and raw bandana paisley block cuts. Everything is screenprinted with heavy discharge ink that sinks directly into the cotton weave instead of sitting like cheap sticky plastic on top.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-6">
            <div className="space-y-2">
              <span className="text-2xl font-black font-display text-neutral-950 dark:text-white block">
                500 GSM
              </span>
              <h3 className="text-xs font-bold uppercase tracking-wider text-neutral-900 dark:text-neutral-100">
                Heavyweight Armor
              </h3>
              <p className="text-xs text-neutral-500">
                Bulletproof fleece weight that refuses to sag or wrinkle.
              </p>
            </div>

            <div className="space-y-2">
              <span className="text-2xl font-black font-display text-neutral-950 dark:text-white block">
                CHICANO
              </span>
              <h3 className="text-xs font-bold uppercase tracking-wider text-neutral-900 dark:text-neutral-100">
                Street Heritage
              </h3>
              <p className="text-xs text-neutral-500">
                Original Old English hand-lettering and authentic lowrider pinstripes.
              </p>
            </div>

            <div className="space-y-2">
              <span className="text-2xl font-black font-display text-neutral-950 dark:text-white block">
                RAW GUM
              </span>
              <h3 className="text-xs font-bold uppercase tracking-wider text-neutral-900 dark:text-neutral-100">
                Skate Cupsole
              </h3>
              <p className="text-xs text-neutral-500">
                Sticky raw gum outsoles engineered for daily street punishment.
              </p>
            </div>
          </div>
        </div>

      </div>

      {/* Return CTA */}
      <div className="mt-20 pt-10 border-t border-neutral-200/60 dark:border-neutral-800/60 flex justify-between items-center">
        <span className="text-xs text-neutral-400 uppercase tracking-widest font-mono">
          HOODOO LOS ANGELES · EST. 2024
        </span>
        <button
          onClick={onBackToCatalog}
          className="px-6 py-3 bg-neutral-950 hover:bg-black text-white dark:bg-white dark:text-neutral-950 dark:hover:bg-neutral-200 rounded-full text-xs font-extrabold uppercase tracking-wider transition-all"
        >
          EXPLORE GEAR
        </button>
      </div>
    </div>
  );
};
