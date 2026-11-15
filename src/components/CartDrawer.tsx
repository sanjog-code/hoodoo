import React, { useState } from 'react';
import type { CartItem } from '../types';
import { X, Trash2, Plus, Minus, ArrowRight, ShieldCheck, Tag } from 'lucide-react';

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  cartItems: CartItem[];
  onUpdateQuantity: (index: number, newQty: number) => void;
  onRemoveItem: (index: number) => void;
  onProceedCheckout: () => void;
}

export const CartDrawer: React.FC<CartDrawerProps> = ({
  isOpen,
  onClose,
  cartItems,
  onUpdateQuantity,
  onRemoveItem,
  onProceedCheckout,
}) => {
  const [promoCode, setPromoCode] = useState('');
  const [appliedDiscount, setAppliedDiscount] = useState<number>(0);
  const [promoError, setPromoError] = useState<string | null>(null);

  if (!isOpen) return null;

  const rawSubtotal = cartItems.reduce(
    (acc, item) => acc + item.product.price * item.quantity,
    0
  );

  const discountAmount = (rawSubtotal * appliedDiscount) / 100;
  const subtotal = Math.max(0, rawSubtotal - discountAmount);
  const freeShippingThreshold = 200;
  const freeShippingMet = subtotal >= freeShippingThreshold;
  const amountToFreeShipping = Math.max(0, freeShippingThreshold - subtotal);
  const shippingProgress = Math.min(100, (subtotal / freeShippingThreshold) * 100);

  const handleApplyPromo = (e: React.FormEvent) => {
    e.preventDefault();
    if (promoCode.trim().toUpperCase() === 'WESTSIDE10') {
      setAppliedDiscount(10);
      setPromoError(null);
    } else if (promoCode.trim().toUpperCase() === 'HOODOO20') {
      setAppliedDiscount(20);
      setPromoError(null);
    } else {
      setPromoError('Invalid code. Try "WESTSIDE10" for 10% off');
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden font-sans">
      <div
        className="absolute inset-0 bg-neutral-950/70 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-white dark:bg-[#0c0c0e] border-l border-neutral-200 dark:border-neutral-800 shadow-2xl flex flex-col justify-between text-neutral-900 dark:text-neutral-100">
          
          <div className="p-6 border-b border-neutral-200 dark:border-neutral-800 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <h2 className="text-lg font-black tracking-tight uppercase font-display">YOUR BAG</h2>
              <span className="px-2.5 py-0.5 rounded-full bg-neutral-100 dark:bg-neutral-800 text-xs font-mono font-bold tabular-nums">
                {cartItems.reduce((acc, i) => acc + i.quantity, 0)} ITEMS
              </span>
            </div>
            <button
              onClick={onClose}
              aria-label="Close bag"
              className="p-2 text-neutral-500 hover:text-black dark:hover:text-white rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="px-6 py-3.5 bg-neutral-50 dark:bg-neutral-900/60 border-b border-neutral-200 dark:border-neutral-800">
            <div className="flex items-center justify-between text-xs font-mono mb-1.5 font-bold">
              <span>
                {freeShippingMet
                  ? '✓ UNLOCKED FREE WORLDWIDE SHIPPING'
                  : `Add $${amountToFreeShipping.toFixed(0)} more for FREE SHIPPING`}
              </span>
              <span className="tabular-nums">{shippingProgress.toFixed(0)}%</span>
            </div>
            <div className="w-full bg-neutral-200 dark:bg-neutral-800 h-1.5 rounded-full overflow-hidden">
              <div
                className="bg-neutral-950 dark:bg-white h-full transition-all duration-300 rounded-full"
                style={{ width: `${shippingProgress}%` }}
              />
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {cartItems.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-3">
                <p className="text-sm font-bold uppercase tracking-wider text-neutral-800 dark:text-neutral-200">
                  Your bag is empty
                </p>
                <p className="text-xs text-neutral-500 max-w-xs">
                  Pick your favorite box-cut heavy hoodie, tee, or low-top kicks from the catalog.
                </p>
              </div>
            ) : (
              cartItems.map((item, idx) => (
                <div
                  key={`${item.product.id}-${item.selectedSize}-${item.selectedColor}-${idx}`}
                  className="flex gap-4 p-3 rounded-2xl bg-neutral-100/60 dark:bg-neutral-900/40 items-center"
                >
                  <img
                    src={item.product.image}
                    alt={item.product.name}
                    className="w-16 h-16 object-contain rounded-xl bg-white dark:bg-neutral-800 p-1"
                  />
                  <div className="flex-1 min-w-0">
                    <h4 className="text-xs font-black uppercase truncate text-neutral-900 dark:text-neutral-100">
                      {item.product.name}
                    </h4>
                    <div className="flex items-center gap-2 text-[11px] font-mono text-neutral-500 mt-0.5">
                      <span>SIZE: {item.selectedSize}</span>
                      <span>•</span>
                      <span className="tabular-nums">${item.product.price}</span>
                    </div>

                    <div className="flex items-center justify-between mt-2">
                      <div className="flex items-center bg-white dark:bg-neutral-800 rounded-lg overflow-hidden border border-neutral-200 dark:border-neutral-700">
                        <button
                          onClick={() => onUpdateQuantity(idx, item.quantity - 1)}
                          aria-label="Decrease quantity"
                          className="w-8 h-8 flex items-center justify-center hover:bg-neutral-100 dark:hover:bg-neutral-700 text-neutral-600 dark:text-neutral-300 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-neutral-400"
                        >
                          <Minus className="w-3.5 h-3.5" />
                        </button>
                        <span className="px-2 text-xs font-mono font-bold tabular-nums min-w-[24px] text-center">
                          {item.quantity}
                        </span>
                        <button
                          onClick={() => onUpdateQuantity(idx, item.quantity + 1)}
                          aria-label="Increase quantity"
                          className="w-8 h-8 flex items-center justify-center hover:bg-neutral-100 dark:hover:bg-neutral-700 text-neutral-600 dark:text-neutral-300 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-neutral-400"
                        >
                          <Plus className="w-3.5 h-3.5" />
                        </button>
                      </div>

                      <button
                        onClick={() => onRemoveItem(idx)}
                        aria-label="Remove item"
                        className="w-8 h-8 flex items-center justify-center text-neutral-400 hover:text-red-500 transition-colors p-1 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {cartItems.length > 0 && (
            <div className="p-6 border-t border-neutral-200 dark:border-neutral-800 bg-neutral-50 dark:bg-neutral-900/60 space-y-4">
              <form onSubmit={handleApplyPromo} className="space-y-1">
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Tag className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" />
                    <input
                      type="text"
                      placeholder="PROMO (Try WESTSIDE10)"
                      value={promoCode}
                      onChange={(e) => setPromoCode(e.target.value)}
                      aria-label="Promo code"
                      className="w-full pl-8 pr-3 py-2 rounded-lg text-xs font-mono uppercase bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
                    />
                  </div>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-neutral-950 hover:bg-black dark:bg-white dark:text-neutral-950 text-white rounded-lg text-xs font-bold font-mono tracking-wider focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 active:scale-95 transition-transform"
                  >
                    APPLY
                  </button>
                </div>
                {promoError && (
                  <p className="text-[10px] text-red-500 font-mono">{promoError}</p>
                )}
                {appliedDiscount > 0 && (
                  <p className="text-[10px] text-emerald-500 font-mono">
                    ✓ {appliedDiscount}% DISCOUNT APPLIED
                  </p>
                )}
              </form>

              <div className="space-y-1.5 text-xs font-mono">
                <div className="flex justify-between text-neutral-500">
                  <span>Subtotal</span>
                  <span className="tabular-nums">${rawSubtotal.toFixed(2)}</span>
                </div>
                {appliedDiscount > 0 && (
                  <div className="flex justify-between text-emerald-600 dark:text-emerald-400">
                    <span>Discount ({appliedDiscount}%)</span>
                    <span className="tabular-nums">-${discountAmount.toFixed(2)}</span>
                  </div>
                )}
                <div className="flex justify-between text-neutral-500">
                  <span>Shipping</span>
                  <span>{freeShippingMet ? 'FREE' : '$15.00'}</span>
                </div>
                <div className="flex justify-between text-base font-bold font-sans pt-2 border-t border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-white">
                  <span>Total</span>
                  <span className="tabular-nums">
                    ${(subtotal + (freeShippingMet ? 0 : 15)).toFixed(2)}
                  </span>
                </div>
              </div>

              <button
                onClick={onProceedCheckout}
                className="w-full py-4 px-4 bg-neutral-950 hover:bg-black text-white dark:bg-white dark:text-neutral-950 dark:hover:bg-neutral-200 rounded-xl font-extrabold text-xs uppercase tracking-wider flex items-center justify-center gap-2 transition-all active:translate-y-[1px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
              >
                <span>PROCEED TO CHECKOUT</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <div className="flex items-center justify-center gap-2 text-[10px] font-mono text-neutral-400">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
                <span>SECURE ENCRYPTED 256-BIT CHECKOUT</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
