import os

# 1. src/components/Footer.tsx
footer_code = '''import React, { useState } from 'react';
import { ArrowRight, Check } from 'lucide-react';

interface FooterProps {
  onNavigate: (page: 'home' | 'about' | 'policy' | 'cookie-policy') => void;
}

export const Footer: React.FC<FooterProps> = ({ onNavigate }) => {
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
              className="inline-block transition-opacity hover:opacity-85"
              aria-label="HOODOO Home"
            >
              <img
                src="/assets/hoodoo_westcoast_logo.png"
                alt="HOODOO"
                className="h-10 w-auto object-contain dark:invert"
              />
            </button>
            <p className="text-sm text-neutral-600 dark:text-neutral-400 max-w-sm leading-relaxed">
              Brutal 500GSM heavyweight street armor forged in Los Angeles. Old English typography, lowrider pinstripes, and raw bandana cuts.
            </p>
            <div className="pt-2 max-w-sm">
              <span className="text-[11px] font-extrabold uppercase tracking-widest text-neutral-500 block mb-2 font-mono">
                LOCK IN FOR PRIVATE BLOCK DROPS
              </span>
              <form onSubmit={handleSubscribe} className="relative flex items-center">
                <input
                  type="email"
                  required
                  placeholder="Drop your email here"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-transparent border-b border-neutral-400 dark:border-neutral-700 pb-2 text-xs text-neutral-900 dark:text-neutral-100 placeholder:text-neutral-500 outline-none focus:border-neutral-950 dark:focus:border-white transition-colors"
                />
                <button
                  type="submit"
                  aria-label="Subscribe"
                  className="absolute right-0 bottom-2 text-neutral-600 hover:text-neutral-950 dark:text-neutral-400 dark:hover:text-white transition-colors"
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
              <span className="font-extrabold uppercase tracking-widest text-neutral-400 text-[11px] font-mono">
                STREET GEAR
              </span>
              <ul className="space-y-2.5 text-neutral-600 dark:text-neutral-400">
                <li>
                  <button onClick={() => onNavigate('home')} className="hover:text-neutral-950 dark:hover:text-white transition-colors">
                    500GSM Heavy Hoodies
                  </button>
                </li>
                <li>
                  <button onClick={() => onNavigate('home')} className="hover:text-neutral-950 dark:hover:text-white transition-colors">
                    Boxy Heavyweight Tees
                  </button>
                </li>
                <li>
                  <button onClick={() => onNavigate('home')} className="hover:text-neutral-950 dark:hover:text-white transition-colors">
                    Raw Gum Skate Kicks
                  </button>
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <span className="font-extrabold uppercase tracking-widest text-neutral-400 text-[11px] font-mono">
                CULTURE
              </span>
              <ul className="space-y-2.5 text-neutral-600 dark:text-neutral-400">
                <li>
                  <button onClick={() => onNavigate('about')} className="hover:text-neutral-950 dark:hover:text-white transition-colors">
                    About The Label
                  </button>
                </li>
                <li>
                  <button onClick={() => onNavigate('about')} className="hover:text-neutral-950 dark:hover:text-white transition-colors">
                    Lowrider & Chicano Roots
                  </button>
                </li>
              </ul>
            </div>

            <div className="space-y-3">
              <span className="font-extrabold uppercase tracking-widest text-neutral-400 text-[11px] font-mono">
                SERVICES
              </span>
              <ul className="space-y-2.5 text-neutral-600 dark:text-neutral-400">
                <li>
                  <button onClick={() => onNavigate('policy')} className="hover:text-neutral-950 dark:hover:text-white transition-colors">
                    Worldwide Shipping
                  </button>
                </li>
                <li>
                  <button onClick={() => onNavigate('cookie-policy')} className="hover:text-neutral-950 dark:hover:text-white transition-colors font-bold">
                    Cookie Policy
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-neutral-500 font-mono">
          <div>
            © {new Date().getFullYear()} HOODOO. LOS ANGELES • COMPTON • EAST LA • VENICE.
          </div>
          <div className="flex items-center gap-6">
            <button onClick={() => onNavigate('cookie-policy')} className="hover:underline">
              Cookie Policy
            </button>
            <button onClick={() => onNavigate('policy')} className="hover:underline">
              Terms
            </button>
            <button onClick={() => onNavigate('about')} className="hover:underline">
              About
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};
'''
with open('src/components/Footer.tsx', 'w', encoding='utf-8') as f:
    f.write(footer_code)

# 2. src/components/CookieBanner.tsx
cookie_banner_code = '''import React, { useState } from 'react';
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
            className="text-neutral-950 dark:text-white font-extrabold underline underline-offset-4 hover:opacity-75"
          >
            cookie policy
          </button>
          <span> to see what cookies are saved and how to control them.</span>
        </div>
        <button
          onClick={() => setIsDismissed(true)}
          className="text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200 p-0.5"
          aria-label="Dismiss cookie notice"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </aside>
  );
};
'''
with open('src/components/CookieBanner.tsx', 'w', encoding='utf-8') as f:
    f.write(cookie_banner_code)

# 3. src/components/CartDrawer.tsx
cart_drawer_code = '''import React, { useState } from 'react';
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
              <span className="px-2.5 py-0.5 rounded-full bg-neutral-100 dark:bg-neutral-800 text-xs font-mono font-bold">
                {cartItems.reduce((acc, i) => acc + i.quantity, 0)} ITEMS
              </span>
            </div>
            <button
              onClick={onClose}
              className="p-2 text-neutral-500 hover:text-black dark:hover:text-white rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
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
              <span>{shippingProgress.toFixed(0)}%</span>
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
                      <span>${item.product.price}</span>
                    </div>

                    <div className="flex items-center justify-between mt-2">
                      <div className="flex items-center bg-white dark:bg-neutral-800 rounded-lg overflow-hidden border border-neutral-200 dark:border-neutral-700">
                        <button
                          onClick={() => onUpdateQuantity(idx, item.quantity - 1)}
                          className="px-2 py-0.5 hover:bg-neutral-100 dark:hover:bg-neutral-700 text-neutral-600 dark:text-neutral-300"
                        >
                          <Minus className="w-3 h-3" />
                        </button>
                        <span className="px-2 text-xs font-mono font-bold">
                          {item.quantity}
                        </span>
                        <button
                          onClick={() => onUpdateQuantity(idx, item.quantity + 1)}
                          className="px-2 py-0.5 hover:bg-neutral-100 dark:hover:bg-neutral-700 text-neutral-600 dark:text-neutral-300"
                        >
                          <Plus className="w-3 h-3" />
                        </button>
                      </div>

                      <button
                        onClick={() => onRemoveItem(idx)}
                        className="text-neutral-400 hover:text-red-500 transition-colors p-1"
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
                      className="w-full pl-8 pr-3 py-1.5 rounded-lg text-xs font-mono uppercase bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 outline-none"
                    />
                  </div>
                  <button
                    type="submit"
                    className="px-4 py-1.5 bg-neutral-950 hover:bg-black dark:bg-white dark:text-neutral-950 text-white rounded-lg text-xs font-bold font-mono tracking-wider"
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
                  <span>${rawSubtotal.toFixed(2)}</span>
                </div>
                {appliedDiscount > 0 && (
                  <div className="flex justify-between text-emerald-600 dark:text-emerald-400">
                    <span>Discount ({appliedDiscount}%)</span>
                    <span>-${discountAmount.toFixed(2)}</span>
                  </div>
                )}
                <div className="flex justify-between text-neutral-500">
                  <span>Shipping</span>
                  <span>{freeShippingMet ? 'FREE' : '$15.00'}</span>
                </div>
                <div className="flex justify-between text-base font-bold font-sans pt-2 border-t border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-white">
                  <span>Total</span>
                  <span>
                    ${(subtotal + (freeShippingMet ? 0 : 15)).toFixed(2)}
                  </span>
                </div>
              </div>

              <button
                onClick={onProceedCheckout}
                className="w-full py-4 px-4 bg-neutral-950 hover:bg-black text-white dark:bg-white dark:text-neutral-950 dark:hover:bg-neutral-200 rounded-xl font-extrabold text-xs uppercase tracking-wider flex items-center justify-center gap-2 transition-all active:translate-y-[1px]"
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
'''
with open('src/components/CartDrawer.tsx', 'w', encoding='utf-8') as f:
    f.write(cart_drawer_code)

# 4. src/components/Toast.tsx
toast_code = '''import React from 'react';
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
'''
with open('src/components/Toast.tsx', 'w', encoding='utf-8') as f:
    f.write(toast_code)

# 5. Fix type imports in other files
# src/data/products.ts
with open('src/data/products.ts', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("import { Product } from '../types';", "import type { Product } from '../types';")
with open('src/data/products.ts', 'w', encoding='utf-8') as f:
    f.write(c)

# src/components/CatalogGrid.tsx
with open('src/components/CatalogGrid.tsx', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("import { Product } from '../types';", "import type { Product } from '../types';")
with open('src/components/CatalogGrid.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

# src/components/HeroSpotlight.tsx
with open('src/components/HeroSpotlight.tsx', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("import { Product } from '../types';", "import type { Product } from '../types';")
with open('src/components/HeroSpotlight.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

# src/components/CheckoutModal.tsx
with open('src/components/CheckoutModal.tsx', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("import { CartItem } from '../types';", "import type { CartItem } from '../types';")
with open('src/components/CheckoutModal.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

# src/App.tsx
app_code = '''import { useState, useEffect } from 'react';
import type { Product, CartItem } from './types';
import { FEATURED_HERO, CATALOG_PRODUCTS } from './data/products';
import { Header } from './components/Header';
import { HeroSpotlight } from './components/HeroSpotlight';
import { CatalogGrid } from './components/CatalogGrid';
import { CartDrawer } from './components/CartDrawer';
import { CheckoutModal } from './components/CheckoutModal';
import { Footer } from './components/Footer';
import { CookieBanner } from './components/CookieBanner';
import { AboutPage } from './pages/AboutPage';
import { PolicyPage } from './pages/PolicyPage';
import { CookiePolicyPage } from './pages/CookiePolicyPage';
import { Toast } from './components/Toast';

export function App() {
  const [currentPage, setCurrentPage] = useState<'home' | 'about' | 'policy' | 'cookie-policy'>('home');
  const [darkMode, setDarkMode] = useState<boolean>(false);
  const [currentHero, setCurrentHero] = useState<Product>(FEATURED_HERO);

  const [cart, setCart] = useState<CartItem[]>([
    {
      product: FEATURED_HERO,
      selectedSize: 'L',
      selectedColor: 'Asphalt Charcoal',
      quantity: 1,
    },
    {
      product: CATALOG_PRODUCTS[0],
      selectedSize: 'XL',
      selectedColor: 'Obsidian Black',
      quantity: 1,
    },
  ]);

  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  const handleAddToCart = (product: Product, size: string, color: string) => {
    setCart((prev) => {
      const idx = prev.findIndex(
        (item) =>
          item.product.id === product.id &&
          item.selectedSize === size &&
          item.selectedColor === color
      );
      if (idx > -1) {
        const copy = [...prev];
        copy[idx].quantity += 1;
        return copy;
      }
      return [...prev, { product, selectedSize: size, selectedColor: color, quantity: 1 }];
    });
    showToast(`Added ${product.name} to bag`);
  };

  const handleQuickAdd = (product: Product) => {
    handleAddToCart(
      product,
      product.sizes[0] || 'L',
      product.swatches?.[0]?.name || 'Standard'
    );
  };

  const handleDirectBuy = (product: Product, size: string, color: string) => {
    handleAddToCart(product, size, color);
    setIsCheckoutOpen(true);
  };

  const handleUpdateQuantity = (idx: number, newQty: number) => {
    if (newQty <= 0) {
      setCart((prev) => prev.filter((_, i) => i !== idx));
      return;
    }
    setCart((prev) => {
      const copy = [...prev];
      copy[idx].quantity = newQty;
      return copy;
    });
  };

  const handleRemoveItem = (idx: number) => {
    setCart((prev) => prev.filter((_, i) => i !== idx));
  };

  const totalCartCount = cart.reduce((acc, item) => acc + item.quantity, 0);

  const navigateTo = (page: 'home' | 'about' | 'policy' | 'cookie-policy') => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f5f5f4] dark:bg-[#0a0a0c] text-neutral-900 dark:text-neutral-100 transition-colors">
      <Header
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        cartCount={totalCartCount}
        onOpenCart={() => setIsCartOpen(true)}
        currentPage={currentPage}
        onNavigate={navigateTo}
      />

      <main className="flex-1 w-full">
        {currentPage === 'home' && (
          <div className="max-w-[1700px] mx-auto px-6 lg:px-12 py-8 lg:py-12">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12 items-start">
              <section className="lg:col-span-5 lg:sticky lg:top-28">
                <HeroSpotlight
                  currentProduct={currentHero}
                  setCurrentProduct={setCurrentHero}
                  onAddToCart={handleAddToCart}
                  onDirectBuy={handleDirectBuy}
                />
              </section>

              <section className="lg:col-span-7">
                <CatalogGrid
                  onSelectProduct={(p: Product) => {
                    setCurrentHero(p);
                    if (window.innerWidth < 1024) {
                      window.scrollTo({ top: 0, behavior: 'smooth' });
                    }
                  }}
                  onQuickAdd={handleQuickAdd}
                  activeSpotlightId={currentHero.id}
                />
              </section>
            </div>
          </div>
        )}

        {currentPage === 'about' && (
          <AboutPage onBackToCatalog={() => navigateTo('home')} />
        )}

        {currentPage === 'policy' && (
          <PolicyPage
            onBackToCatalog={() => navigateTo('home')}
            onNavigateToCookiePolicy={() => navigateTo('cookie-policy')}
          />
        )}

        {currentPage === 'cookie-policy' && (
          <CookiePolicyPage onBackToCatalog={() => navigateTo('home')} />
        )}
      </main>

      <Footer onNavigate={navigateTo} />
      <CookieBanner onNavigateToCookiePolicy={() => navigateTo('cookie-policy')} />

      <CartDrawer
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        cartItems={cart}
        onUpdateQuantity={handleUpdateQuantity}
        onRemoveItem={handleRemoveItem}
        onProceedCheckout={() => {
          setIsCartOpen(false);
          setIsCheckoutOpen(true);
        }}
      />

      <CheckoutModal
        isOpen={isCheckoutOpen}
        onClose={() => setIsCheckoutOpen(false)}
        cartItems={cart}
        onOrderComplete={() => setCart([])}
      />

      <Toast
        message={toastMessage}
        onOpenCart={() => setIsCartOpen(true)}
      />
    </div>
  );
}

export default App;
'''
with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(app_code)

print('All patches applied cleanly!')
