import React from 'react';
import { ArrowLeft, Truck, RotateCcw, ShieldCheck, HeartHandshake } from 'lucide-react';

interface PolicyPageProps {
  onBackToCatalog: () => void;
  onNavigateToCookiePolicy: () => void;
}

export const PolicyPage: React.FC<PolicyPageProps> = ({
  onBackToCatalog,
  onNavigateToCookiePolicy,
}) => {
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
        <span className="text-xs font-bold tracking-widest text-neutral-400 uppercase font-mono">
          CLIENT CARE & DISPATCH RULES
        </span>
        <h1 className="text-4xl sm:text-5xl font-black uppercase tracking-tight font-display text-neutral-950 dark:text-white leading-[1.1]">
          SHIPPING, EXCHANGES & CARE
        </h1>
        <p className="text-base text-neutral-600 dark:text-neutral-300">
          Straightforward policies. Zero runarounds. Tracked express dispatch on every single order.
        </p>
      </div>

      {/* Policy Details Grid */}
      <div className="space-y-12 divide-y divide-neutral-200/60 dark:divide-neutral-800/60">
        
        {/* Shipping */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4 flex items-center gap-3">
            <Truck className="w-5 h-5 text-neutral-950 dark:text-white" />
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              WORLDWIDE SHIPPING
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              Orders are boxed and dispatched within 24 to 48 business hours via DHL Express or FedEx Priority.
            </p>
            <ul className="list-disc list-inside space-y-1 text-neutral-500 dark:text-neutral-400 text-xs">
              <li>US Domestic Delivery: 2 to 4 business days.</li>
              <li>International Express: 3 to 6 business days with tracked door-to-door delivery.</li>
              <li>Free shipping is automatically applied on all orders exceeding $200.</li>
            </ul>
          </div>
        </div>

        {/* Returns & Exchanges */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4 flex items-center gap-3">
            <RotateCcw className="w-5 h-5 text-neutral-950 dark:text-white" />
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              14-DAY EXCHANGES
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              Got the wrong size? We offer exchanges or store credit within 14 calendar days of delivery as long as the garment is unwashed and in original condition.
            </p>
            <p className="text-xs text-neutral-500 dark:text-neutral-400">
              Email concierge at <span className="font-mono font-bold text-neutral-950 dark:text-white">support@hoodoo.studio</span> with your order number.
            </p>
          </div>
        </div>

        {/* Garment Care */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4 flex items-center gap-3">
            <HeartHandshake className="w-5 h-5 text-neutral-950 dark:text-white" />
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              500GSM GARMENT CARE
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              Our heavyweight fleece is nearly indestructible. Wash cold inside-out, hang dry to keep the heavyweight fibers tight and stiff.
            </p>
          </div>
        </div>

        {/* Privacy & Cookie Notice */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4 flex items-center gap-3">
            <ShieldCheck className="w-5 h-5 text-neutral-950 dark:text-white" />
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              PRIVACY & DATA
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              Payments are 256-bit encrypted. We never sell your personal information. Read our dedicated{' '}
              <button
                onClick={onNavigateToCookiePolicy}
                className="underline underline-offset-4 text-neutral-950 dark:text-white font-bold"
              >
                Cookie Policy
              </button>
              {' '}to learn how session storage is used.
            </p>
          </div>
        </div>

      </div>

      {/* Return CTA */}
      <div className="mt-20 pt-10 border-t border-neutral-200/60 dark:border-neutral-800/60 flex justify-between items-center">
        <span className="text-xs text-neutral-400 uppercase tracking-widest font-mono">
          QUESTIONS? CONCIERGE@HOODOO.STUDIO
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
