import React from 'react';
import { ArrowLeft, Cookie } from 'lucide-react';

interface CookiePolicyPageProps {
  onBackToCatalog: () => void;
}

export const CookiePolicyPage: React.FC<CookiePolicyPageProps> = ({ onBackToCatalog }) => {
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

      {/* Hero Header */}
      <div className="space-y-4 max-w-3xl mb-16">
        <span className="text-xs font-bold tracking-widest text-neutral-400 uppercase font-mono flex items-center gap-2">
          <Cookie className="w-4 h-4" />
          LEGAL & TRANSPARENCY
        </span>
        <h1 className="text-4xl sm:text-5xl font-black uppercase tracking-tight font-display text-neutral-950 dark:text-white leading-[1.1]">
          COOKIE POLICY
        </h1>
        <p className="text-base text-neutral-600 dark:text-neutral-300">
          Last updated: November 2026. This policy explains what cookies are, how HOODOO uses them, and how you can manage them in your browser.
        </p>
      </div>

      {/* Main Content Sections */}
      <div className="space-y-12 divide-y divide-neutral-200/60 dark:divide-neutral-800/60">
        
        {/* 1. What are cookies */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4">
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              1. WHAT ARE COOKIES?
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              Cookies are tiny text files placed on your device to ensure website features work correctly, remember what is in your shopping bag, and preserve your visual settings.
            </p>
          </div>
        </div>

        {/* 2. What cookies HOODOO uses */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4">
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              2. COOKIES WE USE
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-4">
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-neutral-100/70 dark:bg-neutral-900/60 space-y-1">
                <div className="flex items-center justify-between font-mono text-xs font-bold text-neutral-900 dark:text-neutral-100">
                  <span>hoodoo_cart</span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-bold">Essential</span>
                </div>
                <p className="text-xs text-neutral-500">
                  Maintains your selected hoodies, sizes, and quantities in the bag across browsing sessions.
                </p>
                <div className="text-[10px] font-mono text-neutral-400">Duration: 30 days</div>
              </div>

              <div className="p-4 rounded-2xl bg-neutral-100/70 dark:bg-neutral-900/60 space-y-1">
                <div className="flex items-center justify-between font-mono text-xs font-bold text-neutral-900 dark:text-neutral-100">
                  <span>hoodoo_theme</span>
                  <span className="text-neutral-600 dark:text-neutral-300 font-bold">Preference</span>
                </div>
                <p className="text-xs text-neutral-500">
                  Saves your preference between Light Mode and Dark Mode.
                </p>
                <div className="text-[10px] font-mono text-neutral-400">Duration: 1 year</div>
              </div>

              <div className="p-4 rounded-2xl bg-neutral-100/70 dark:bg-neutral-900/60 space-y-1">
                <div className="flex items-center justify-between font-mono text-xs font-bold text-neutral-900 dark:text-neutral-100">
                  <span>session_telemetry</span>
                  <span className="text-neutral-600 dark:text-neutral-300 font-bold">Anonymous</span>
                </div>
                <p className="text-xs text-neutral-500">
                  Measures page loading performance without recording personal identity.
                </p>
                <div className="text-[10px] font-mono text-neutral-400">Duration: Session only</div>
              </div>
            </div>
          </div>
        </div>

        {/* 3. Managing Cookies */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4">
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              3. CONTROLLING COOKIES
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              You can inspect or delete cookies anytime in your browser settings under Privacy & Security (Chrome, Safari, Firefox, Edge).
            </p>
          </div>
        </div>

      </div>

      {/* Return CTA */}
      <div className="mt-20 pt-10 border-t border-neutral-200/60 dark:border-neutral-800/60 flex justify-between items-center">
        <span className="text-xs text-neutral-400 uppercase tracking-widest font-mono">
          LEGAL NOTICE · HOODOO
        </span>
        <button
          onClick={onBackToCatalog}
          className="px-6 py-3 bg-neutral-950 hover:bg-black text-white dark:bg-white dark:text-neutral-950 dark:hover:bg-neutral-200 rounded-full text-xs font-extrabold uppercase tracking-wider transition-all"
        >
          RETURN TO CATALOG
        </button>
      </div>
    </div>
  );
};
