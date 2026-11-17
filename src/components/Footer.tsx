import React, { useState } from 'react';
import { ArrowRight, Check } from 'lucide-react';
import { HoodooLogo, BrandPalette } from './HoodooLogo';

interface FooterProps {
  onNavigate: (page: 'home' | 'about' | 'policy' | 'cookie-policy') => void;
  palette?: BrandPalette;
}

export const Footer: React.FC<FooterProps> = ({ onNavigate, palette = 'cobalt' }) => {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    if (email.trim()) {
      setSubscribed(true);
      setTimeout(() => {
        setEmail('');
        setSubscribed(false);
      }, 4000);
    }
  };

  return (
    <footer className="mt-20 pt-16 pb-12 bg-neutral-200/50 dark:bg-[#08080a] text-neutral-800 dark:text-neutral-200 transition-colors border-t border-neutral-300/40 dark:border-neutral-800/40">
      <div className="max-w-[1600px] mx-auto px-6 lg:px-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-12 lg:gap-16 pb-16 border-b border-neutral-300/50 dark:border-neutral-800/60">
          <div className="lg:col-span-5 space-y-6">
            <button
              onClick={() => onNavigate('home')}
              className="inline-block transition-opacity hover:opacity-85 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm"
              aria-label="HOODOO Home"
            >
              <HoodooLogo size="md" palette={palette} />
            </button>
            <p className="text-sm text-neutral-600 dark:text-neutral-400 max-w-sm leading-relaxed">
              Brutal 500GSM heavyweight street armor forged in Los Angeles. Old English typography, lowrider pinstripes, and raw bandana cuts.
            </p>
            <div className="pt-2 max-w-sm">
              <span className="text-[11px] font-extrabold uppercase tracking-widest text-neutral-500 block mb-2 font-mono">
                LOCK IN FOR PRIVATE ARCHIVE RELEASES
              </span>
              <form onSubmit={handleSubscribe} className="relative flex items-center">
                <input
                  type="email"
                  required
                  placeholder="Enter your email here"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-transparent border-b border-neutral-400 dark:border-neutral-700 pb-2 text-xs text-neutral-900 dark:text-neutral-100 placeholder:text-neutral-500 outline-none focus:border-neutral-950 dark:focus:border-white transition-colors"
                />
                <button
                  type="submit"
                  aria-label="Subscribe to archive newsletter"
                  className="absolute right-0 bottom-2 text-neutral-600 hover:text-neutral-950 dark:text-neutral-400 dark:hover:text-white transition-colors p-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm"
                >
                  {subscribed ? (
                    <Check className="w-4 h-4 text-emerald-500" />
                  ) : (
                    <ArrowRight className="w-4 h-4" />
                  )}
                </button>
              </form>
              {subscribed && (
                <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono mt-1.5 block font-bold">
                  ✓ LOCKED IN. YOU'RE ON THE LIST.
                </span>
              )}
            </div>
          </div>

          <div className="lg:col-span-7 grid grid-cols-2 sm:grid-cols-3 gap-8 text-xs font-semibold">
            <div className="space-y-3">
              <span className="font-extrabold uppercase tracking-widest text-neutral-500 dark:text-neutral-400 text-[11px] font-mono">
                STREET GEAR
              </span>
              <ul className="space-y-2.5 text-neutral-700 dark:text-neutral-300">
                <li>
                  <button onClick={() => onNavigate('home')} className="hover:text-neutral-950 dark:hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm">
                    500GSM Heavy Hoodies
                  </button>
                </li>
                <li>
                  <button onClick={() => onNavigate('home')} className="hover:text-neutral-950 dark:hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm">
                    Boxy Heavyweight Tees
                  </button>
                </li>
                <li>
                  <button onClick={() => onNavigate('home')} className="hover:text-neutral-950 dark:hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm">
                    Raw Gum Skate Kicks
                  </button>
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <span className="font-extrabold uppercase tracking-widest text-neutral-500 dark:text-neutral-400 text-[11px] font-mono">
                CULTURE
              </span>
              <ul className="space-y-2.5 text-neutral-700 dark:text-neutral-300">
                <li>
                  <button onClick={() => onNavigate('about')} className="hover:text-neutral-950 dark:hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm">
                    About The Label
                  </button>
                </li>
                <li>
                  <button onClick={() => onNavigate('about')} className="hover:text-neutral-950 dark:hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm">
                    Lowrider & Chicano Roots
                  </button>
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <span className="font-extrabold uppercase tracking-widest text-neutral-500 dark:text-neutral-400 text-[11px] font-mono">
                SERVICES
              </span>
              <ul className="space-y-2.5 text-neutral-700 dark:text-neutral-300">
                <li>
                  <button onClick={() => onNavigate('policy')} className="hover:text-neutral-950 dark:hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm">
                    Worldwide Shipping
                  </button>
                </li>
                <li>
                  <button onClick={() => onNavigate('cookie-policy')} className="hover:text-neutral-950 dark:hover:text-white transition-colors font-bold focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm">
                    Cookie Policy
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-neutral-600 dark:text-neutral-400 font-mono">
          <div>
            © {new Date().getFullYear()} HOODOO. LOS ANGELES • COMPTON • EAST LA • VENICE.
          </div>
          <div className="flex items-center gap-6">
            <button onClick={() => onNavigate('cookie-policy')} className="hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm">
              Cookie Policy
            </button>
            <button onClick={() => onNavigate('policy')} className="hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm">
              Terms
            </button>
            <button onClick={() => onNavigate('about')} className="hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm">
              About
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};
