import React, { useState } from 'react';
import { X, Cookie } from 'lucide-react';

interface CookieBannerProps {
  onNavigateToCookiePolicy: () => void;
}

export const CookieBanner: React.FC<CookieBannerProps> = ({ onNavigateToCookiePolicy }) => {
  const [isDismissed, setIsDismissed] = useState(false);

  if (isDismissed) return null;

  return (
    <aside aria-label="Cookie statement" className="fixed bottom-4 left-4 right-4 sm:left-8 sm:right-auto sm:max-w-md z-40">
      <div className="bg-white/95 dark:bg-[#121215]/95 backdrop-blur-md text-neutral-800 dark:text-neutral-200 text-xs px-4 py-3.5 rounded-2xl shadow-xl flex items-start gap-3 border border-neutral-200/50 dark:border-neutral-800/60">
        <Cookie className="w-4 h-4 text-neutral-900 dark:text-neutral-100 shrink-0 mt-0.5" />
        <div className="flex-1 leading-relaxed">
          <span>We use cookies to maintain your shopping bag across pages and remember your view mode. Read our </span>
          <button
            onClick={onNavigateToCookiePolicy}
            className="text-neutral-950 dark:text-white font-extrabold underline underline-offset-4 hover:opacity-75 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm"
          >
            cookie policy
          </button>
          <span> to see what cookies are saved and how to control them.</span>
        </div>
        <button
          onClick={() => setIsDismissed(true)}
          className="text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 p-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm"
          aria-label="Dismiss cookie notice"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </aside>
  );
};
