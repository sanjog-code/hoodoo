import React, { useState } from 'react';
import { X, Trash2, ShoppingBag, Check, Sparkles, Flame, Tag } from 'lucide-react';
import { MenuItem } from './KrunchMenu';
import { ReactiveButton, sfx } from './ReactiveButton';

export interface CartItem {
  item: MenuItem;
  quantity: number;
}

interface KrunchCartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  cartItems: CartItem[];
  onUpdateQuantity: (id: string, delta: number) => void;
  onClearCart: () => void;
}

export const KrunchCartDrawer: React.FC<KrunchCartDrawerProps> = ({
  isOpen,
  onClose,
  cartItems,
  onUpdateQuantity,
  onClearCart,
}) => {
  const [promoCode, setPromoCode] = useState<string>('');
  const [discountPercent, setDiscountPercent] = useState<number>(0);
  const [promoError, setPromoError] = useState<string | null>(null);
  const [orderConfirmed, setOrderConfirmed] = useState<boolean>(false);
  const [confirmedTicketNum, setConfirmedTicketNum] = useState<number>(777);

  if (!isOpen) return null;

  const subtotal = cartItems.reduce((sum, ci) => sum + ci.item.price * ci.quantity, 0);
  const discountAmount = subtotal * (discountPercent / 100);
  const taxable = Math.max(0, subtotal - discountAmount);
  const tax = taxable * 0.0825;
  const total = taxable + tax;

  const handleApplyPromo = () => {
    const code = promoCode.trim().toUpperCase();
    if (code === 'BIGMOUTH20' || code === 'KRUNCH20') {
      setDiscountPercent(20);
      setPromoError(null);
      sfx.playCrunch();
    } else if (code === 'SMASH10') {
      setDiscountPercent(10);
      setPromoError(null);
      sfx.playCrunch();
    } else {
      setPromoError('Invalid code. Try: BIGMOUTH20');
      sfx.playPop(300);
    }
  };

  const handleCheckout = () => {
    sfx.playCrunch();
    setConfirmedTicketNum(Math.floor(100 + Math.random() * 900));
    setOrderConfirmed(true);
  };

  const handleCloseAll = () => {
    if (orderConfirmed) {
      onClearCart();
      setOrderConfirmed(false);
      setDiscountPercent(0);
      setPromoCode('');
    }
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden flex justify-end">
      {/* Backdrop */}
      <div
        onClick={handleCloseAll}
        className="absolute inset-0 bg-black/80 backdrop-blur-sm transition-opacity"
      />

      {/* Drawer Panel */}
      <div className="relative w-full max-w-md bg-neutral-950 border-l border-neutral-800 h-full shadow-2xl flex flex-col z-10 text-white font-sans">
        
        {/* Drawer Header */}
        <div className="p-6 border-b border-neutral-800 flex items-center justify-between bg-neutral-900/60">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
              <ShoppingBag className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-black text-lg text-white font-sans tracking-tight">
                THE BITE BAG
              </h3>
              <span className="text-[10px] font-mono text-neutral-400 uppercase tracking-widest">
                {cartItems.reduce((acc, ci) => acc + ci.quantity, 0)} ITEMS SELECTED
              </span>
            </div>
          </div>

          <button
            onClick={handleCloseAll}
            className="p-2 rounded-lg bg-neutral-900 border border-neutral-800 text-neutral-400 hover:text-white transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* ORDER CONFIRMATION VIEW */}
        {orderConfirmed ? (
          <div className="flex-1 p-6 flex flex-col items-center justify-center text-center overflow-y-auto">
            <div className="w-16 h-16 rounded-2xl bg-amber-500/20 border-2 border-amber-500 flex items-center justify-center text-amber-400 mb-4 animate-bounce">
              <Flame className="w-8 h-8" />
            </div>

            <div className="px-3 py-1 rounded-full bg-lime-400/10 border border-lime-400/30 text-lime-400 font-mono text-xs font-bold uppercase tracking-wider mb-2">
              ● TRANSMITTED TO 475°F CAST IRON
            </div>

            <h2 className="text-3xl font-black text-white font-sans">
              ORDER #{confirmedTicketNum}
            </h2>
            <p className="text-neutral-400 text-xs sm:text-sm mt-2 max-w-xs leading-relaxed">
              Your burgers have hit the griddle! Sizzling fresh in East Austin. Estimated pickup is <strong>12 to 15 minutes</strong>.
            </p>

            {/* Receipt Card */}
            <div className="w-full mt-6 p-4 rounded-xl bg-neutral-900 border border-neutral-800 font-mono text-xs text-left space-y-2">
              <div className="flex justify-between text-neutral-400 pb-2 border-b border-neutral-800">
                <span>STATION:</span>
                <span className="text-amber-400 font-bold">GRIDDLE BAY #01</span>
              </div>
              <div className="flex justify-between text-neutral-400">
                <span>ESTIMATED READY:</span>
                <span className="text-white font-bold">14 MINUTES</span>
              </div>
              <div className="flex justify-between text-neutral-400 pt-2 border-t border-neutral-800">
                <span>TOTAL PAID:</span>
                <span className="text-amber-400 font-bold tabular-nums">${total.toFixed(2)}</span>
              </div>
            </div>

            <button
              onClick={handleCloseAll}
              className="mt-8 w-full py-3.5 rounded-xl bg-amber-500 text-neutral-950 font-black text-sm uppercase tracking-wider hover:bg-amber-400 transition-colors shadow-lg shadow-amber-500/20"
            >
              CHOMP DONE • CLOSE TICKET
            </button>
          </div>
        ) : (
          /* CART ITEMS LIST */
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {cartItems.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center text-neutral-500">
                <ShoppingBag className="w-12 h-12 stroke-[1.5] mb-3 text-neutral-600" />
                <h4 className="font-bold text-white text-base">Your Bite Bag is empty!</h4>
                <p className="text-xs text-neutral-400 mt-1 max-w-xs">
                  Hit the menu and chomp on some 44 Farms smashed patties or hand-spun custards.
                </p>
              </div>
            ) : (
              cartItems.map(({ item, quantity }) => (
                <div
                  key={item.id}
                  className="p-4 rounded-xl bg-neutral-900/80 border border-neutral-800 flex items-center justify-between gap-4"
                >
                  <div className="w-14 h-14 rounded-lg overflow-hidden flex-shrink-0 bg-neutral-800 border border-neutral-700">
                    <img src={item.image} alt={item.name} className="w-full h-full object-cover" />
                  </div>

                  <div className="flex-1 min-w-0">
                    <h4 className="font-bold text-sm text-white truncate font-sans">
                      {item.name}
                    </h4>
                    <div className="text-xs font-mono text-amber-400 font-bold tabular-nums">
                      ${item.price.toFixed(2)} each
                    </div>
                  </div>

                  {/* Quantity Stepper */}
                  <div className="flex items-center gap-2 bg-neutral-950 p-1 rounded-lg border border-neutral-800">
                    <button
                      onClick={() => onUpdateQuantity(item.id, -1)}
                      className="w-6 h-6 rounded flex items-center justify-center text-neutral-400 hover:text-white transition-colors"
                    >
                      −
                    </button>
                    <span className="font-mono text-xs font-bold text-white min-w-4 text-center tabular-nums">
                      {quantity}
                    </span>
                    <button
                      onClick={() => onUpdateQuantity(item.id, 1)}
                      className="w-6 h-6 rounded flex items-center justify-center text-neutral-400 hover:text-white transition-colors"
                    >
                      +
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {/* Drawer Footer (Summary & Checkout) */}
        {!orderConfirmed && cartItems.length > 0 && (
          <div className="p-6 border-t border-neutral-800 bg-neutral-900/80 space-y-4">
            
            {/* Promo Code Input */}
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Tag className="w-4 h-4 text-neutral-500 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={promoCode}
                  onChange={(e) => setPromoCode(e.target.value)}
                  placeholder="CODE (e.g. BIGMOUTH20)"
                  className="w-full pl-9 pr-3 py-2 bg-neutral-950 border border-neutral-800 rounded-lg text-xs font-mono text-white placeholder-neutral-500 uppercase focus:outline-none focus:border-amber-400"
                />
              </div>
              <button
                onClick={handleApplyPromo}
                className="px-4 py-2 rounded-lg bg-neutral-800 border border-neutral-700 text-xs font-mono font-bold hover:text-white hover:border-amber-400 transition-colors"
              >
                APPLY
              </button>
            </div>

            {/* Promo Status Feedback */}
            {discountPercent > 0 && (
              <div className="text-xs font-mono text-lime-400 flex items-center gap-1">
                <Check className="w-3.5 h-3.5" />
                <span>{discountPercent}% GEN Z VIP DISCOUNT APPLIED!</span>
              </div>
            )}
            {promoError && (
              <div className="text-xs font-mono text-red-400">
                {promoError}
              </div>
            )}

            {/* Calculations Breakdown */}
            <div className="space-y-1.5 text-xs font-mono">
              <div className="flex justify-between text-neutral-400">
                <span>SUBTOTAL:</span>
                <span className="text-white tabular-nums">${subtotal.toFixed(2)}</span>
              </div>

              {discountPercent > 0 && (
                <div className="flex justify-between text-lime-400">
                  <span>DISCOUNT ({discountPercent}%):</span>
                  <span className="tabular-nums">-${discountAmount.toFixed(2)}</span>
                </div>
              )}

              <div className="flex justify-between text-neutral-400">
                <span>TEXAS TAX (8.25%):</span>
                <span className="text-white tabular-nums">${tax.toFixed(2)}</span>
              </div>

              <div className="flex justify-between text-base font-black font-sans text-white pt-2 border-t border-neutral-800">
                <span>TOTAL:</span>
                <span className="text-amber-400 font-mono tabular-nums">${total.toFixed(2)}</span>
              </div>
            </div>

            {/* Checkout Action Button */}
            <button
              onClick={handleCheckout}
              className="w-full py-4 rounded-xl bg-gradient-to-r from-amber-500 via-orange-500 to-amber-500 text-neutral-950 font-black text-sm uppercase tracking-wider hover:brightness-110 active:translate-y-[2px] transition-all shadow-xl shadow-amber-500/25 flex items-center justify-center gap-2"
            >
              <Flame className="w-4 h-4 fill-neutral-950" />
              <span>TRANSMIT ORDER TO FLAT-TOP (${total.toFixed(2)})</span>
            </button>
          </div>
        )}

      </div>
    </div>
  );
};
