import React from 'react';
import { CheckCircle2, ShoppingBag } from 'lucide-react';

interface ToastProps {
  message: string | null;
  onOpenCart: () => void;
}

export const Toast: React.FC<ToastProps> = ({ message, onOpenCart }) => {
  if (!message) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className="bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 px-4 py-3 rounded-2xl shadow-2xl flex items-center gap-3 font-sans border border-neutral-800 dark:border-neutral-200">
        <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
        <span className="text-xs font-bold uppercase tracking-wider">{message}</span>
        <button
          onClick={onOpenCart}
          className="ml-2 text-xs font-mono font-bold underline underline-offset-2 flex items-center gap-1 opacity-80 hover:opacity-100"
        >
          <ShoppingBag className="w-3.5 h-3.5" /> Bag
        </button>
      </div>
    </div>
  );
};
