import React, { useState, useEffect } from 'react';
import type { CartItem } from '../types';
import { X, CheckCircle2, Lock, CreditCard, ArrowRight } from 'lucide-react';

interface CheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  cartItems: CartItem[];
  onOrderComplete: () => void;
}

export const CheckoutModal: React.FC<CheckoutModalProps> = ({
  isOpen,
  onClose,
  cartItems,
  onOrderComplete,
}) => {
  const [step, setStep] = useState<'details' | 'success'>('details');
  const [email, setEmail] = useState('westside@hoodoo.studio');
  const [name, setName] = useState('Marcus Vance');
  const [address, setAddress] = useState('1042 Crenshaw Blvd, Los Angeles, CA 90019');
  const [cardNumber, setCardNumber] = useState('•••• •••• •••• 4242');
  const [isProcessing, setIsProcessing] = useState(false);
  const [orderId, setOrderId] = useState('');

  const resetAndClose = () => {
    setStep('details');
    onClose();
  };

  // Close modal on Escape key press (WCAG 2.1.2 compliance)
  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') resetAndClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  if (!isOpen) return null;

  const total = cartItems.reduce(
    (acc, item) => acc + item.product.price * item.quantity,
    0
  );

  const handlePay = (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      setOrderId(`LA-${Math.floor(100000 + Math.random() * 900000)}`);
      setStep('success');
      onOrderComplete();
    }, 1200);
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 font-sans"
      role="dialog"
      aria-modal="true"
      aria-labelledby="checkout-modal-title"
    >
      <div
        className="absolute inset-0 bg-neutral-950/80 backdrop-blur-sm"
        onClick={resetAndClose}
        aria-hidden="true"
      />
      <div className="relative w-full max-w-lg bg-white dark:bg-[#0c0c0e] border border-neutral-200 dark:border-neutral-800 rounded-3xl shadow-2xl p-6 sm:p-8 max-h-[90vh] overflow-y-auto text-neutral-900 dark:text-neutral-100">
        
        {/* Close Button */}
        <button
          onClick={resetAndClose}
          aria-label="Close checkout modal"
          className="absolute top-5 right-5 p-2 rounded-lg text-neutral-400 hover:text-black dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
        >
          <X className="w-5 h-5" />
        </button>

        {step === 'details' ? (
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Lock className="w-4 h-4 text-emerald-500" />
              <span className="text-xs font-mono font-bold tracking-widest text-neutral-600 dark:text-neutral-400 uppercase">
                EXPRESS STREET CHECKOUT
              </span>
            </div>
            <h2 id="checkout-modal-title" className="text-2xl font-black uppercase tracking-tight text-neutral-950 dark:text-white font-display">
              CONFIRM GEAR & DISPATCH
            </h2>

            {/* Order Items Snapshot */}
            <div className="my-5 p-4 rounded-2xl bg-neutral-50 dark:bg-neutral-900/60 divide-y divide-neutral-200/60 dark:divide-neutral-800">
              {cartItems.map((item, idx) => (
                <div key={idx} className="py-2.5 first:pt-0 last:pb-0 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-3">
                    <img src={item.product.image} alt={item.product.name} className="w-10 h-10 object-contain rounded-lg bg-white dark:bg-neutral-800 p-0.5" />
                    <div>
                      <p className="font-bold uppercase truncate max-w-[200px]">{item.product.name}</p>
                      <p className="text-[10px] text-neutral-600 dark:text-neutral-400 font-mono">Qty: {item.quantity} | Size: {item.selectedSize}</p>
                    </div>
                  </div>
                  <span className="font-mono font-bold tabular-nums">${item.product.price * item.quantity}</span>
                </div>
              ))}
              <div className="pt-3 flex justify-between font-extrabold text-sm font-sans">
                <span>TOTAL DUE</span>
                <span className="tabular-nums">${total.toFixed(2)}</span>
              </div>
            </div>

            {/* Shipping & Payment Form */}
            <form onSubmit={handlePay} className="space-y-3.5 text-xs font-mono">
              <div>
                <label className="block text-[11px] font-bold text-neutral-800 dark:text-neutral-200 mb-1">
                  EMAIL FOR TRACKING
                </label>
                <input
                  type="email"
                  required
                  aria-required="true"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  aria-label="Email for tracking"
                  className="w-full px-3 py-2 rounded-xl bg-neutral-100/70 dark:bg-neutral-900 border border-neutral-300 dark:border-neutral-700 outline-none focus:border-neutral-950 dark:focus:border-white text-neutral-900 dark:text-neutral-100 focus-visible:ring-2 focus-visible:ring-neutral-400"
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold text-neutral-800 dark:text-neutral-200 mb-1">
                  RECIPIENT NAME
                </label>
                <input
                  type="text"
                  required
                  aria-required="true"
                  autoComplete="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  aria-label="Recipient name"
                  className="w-full px-3 py-2 rounded-xl bg-neutral-100/70 dark:bg-neutral-900 border border-neutral-300 dark:border-neutral-700 outline-none focus:border-neutral-950 dark:focus:border-white text-neutral-900 dark:text-neutral-100 focus-visible:ring-2 focus-visible:ring-neutral-400"
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold text-neutral-800 dark:text-neutral-200 mb-1">
                  DELIVERY ADDRESS
                </label>
                <input
                  type="text"
                  required
                  aria-required="true"
                  autoComplete="street-address"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  aria-label="Delivery address"
                  className="w-full px-3 py-2 rounded-xl bg-neutral-100/70 dark:bg-neutral-900 border border-neutral-300 dark:border-neutral-700 outline-none focus:border-neutral-950 dark:focus:border-white text-neutral-900 dark:text-neutral-100 focus-visible:ring-2 focus-visible:ring-neutral-400"
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold text-neutral-800 dark:text-neutral-200 mb-1 flex items-center justify-between">
                  <span>PAYMENT CARD</span>
                  <span className="flex items-center gap-1 text-[10px] text-neutral-500 dark:text-neutral-400">
                    <CreditCard className="w-3 h-3" /> Encrypted Sandbox
                  </span>
                </label>
                <input
                  type="text"
                  autoComplete="cc-number"
                  value={cardNumber}
                  onChange={(e) => setCardNumber(e.target.value)}
                  aria-label="Payment card number"
                  className="w-full px-3 py-2 rounded-xl bg-neutral-100/70 dark:bg-neutral-900 border border-neutral-300 dark:border-neutral-700 outline-none text-neutral-900 dark:text-neutral-100 focus-visible:ring-2 focus-visible:ring-neutral-400"
                />
              </div>

              <button
                type="submit"
                disabled={isProcessing}
                className="w-full mt-4 py-4 px-4 bg-neutral-950 hover:bg-black text-white dark:bg-white dark:text-neutral-950 dark:hover:bg-neutral-200 rounded-xl font-extrabold font-sans text-xs uppercase tracking-wider flex items-center justify-center gap-2 transition-all active:translate-y-[1px] disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
              >
                {isProcessing ? (
                  <span className="animate-pulse">DISPATCHING ORDER...</span>
                ) : (
                  <>
                    <span className="tabular-nums">CONFIRM & DISPATCH • ${total.toFixed(2)}</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>
          </div>
        ) : (
          <div className="text-center py-6 space-y-4">
            <div className="w-16 h-16 rounded-full bg-emerald-500/10 text-emerald-500 mx-auto flex items-center justify-center">
              <CheckCircle2 className="w-10 h-10 stroke-[2]" />
            </div>

            <div>
              <span className="text-xs font-mono font-bold tracking-widest text-neutral-600 dark:text-neutral-400 uppercase">
                ORDER DISPATCHED
              </span>
              <h2 className="text-2xl font-black uppercase tracking-tight text-neutral-950 dark:text-white mt-1 font-display">
                ORDER DISPATCH CONFIRMED
              </h2>
            </div>

            <p className="text-xs text-neutral-700 dark:text-neutral-300 max-w-xs mx-auto leading-relaxed">
              Order <strong>{orderId}</strong> is prepped for dispatch. Tracking details will be emailed to <strong>{email}</strong>.
            </p>

            <button
              onClick={resetAndClose}
              className="w-full py-4 px-4 bg-neutral-950 hover:bg-black dark:bg-white dark:text-neutral-950 dark:hover:bg-neutral-200 text-white rounded-xl font-extrabold font-sans text-xs uppercase tracking-wider transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
            >
              BACK TO GEAR
            </button>
          </div>
        )}

      </div>
    </div>
  );
};
