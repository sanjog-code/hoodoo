import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { HeroSpotlight } from './components/HeroSpotlight';
import { CatalogGrid } from './components/CatalogGrid';
import { ThreeDStudioModal } from './components/ThreeDStudioModal';
import { CartDrawer } from './components/CartDrawer';
import { CheckoutModal } from './components/CheckoutModal';
import { Footer } from './components/Footer';
import { CookieBanner } from './components/CookieBanner';
import { Toast } from './components/Toast';
import { AboutPage } from './pages/AboutPage';
import { PolicyPage } from './pages/PolicyPage';
import { CookiePolicyPage } from './pages/CookiePolicyPage';
import { FEATURED_HERO, CATALOG_PRODUCTS } from './data/products';
import type { Product, CartItem } from './types';
import type { BrandPalette } from './components/HoodooLogo';

export function App() {
  const [darkMode, setDarkMode] = useState<boolean>(true);
  const [palette, setPalette] = useState<BrandPalette>('silver');
  const [currentPage, setCurrentPage] = useState<'home' | 'about' | 'policy' | 'cookie-policy'>('home');
  
  const [cart, setCart] = useState<CartItem[]>(() => {
    try {
      const saved = localStorage.getItem('hoodoo_cart');
      if (saved) return JSON.parse(saved);
    } catch (e) {
      // ignore
    }
    return [
      {
        product: FEATURED_HERO,
        selectedSize: 'L',
        selectedColor: 'Asphalt Charcoal',
        quantity: 1,
      },
    ];
  });

  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);
  const [currentHeroProduct, setCurrentHeroProduct] = useState<Product>(FEATURED_HERO);
  
  // 3D Studio modal state
  const [is3DModalOpen, setIs3DModalOpen] = useState(false);
  const [studioProduct, setStudioProduct] = useState<Product>(FEATURED_HERO);
  const [studioColor, setStudioColor] = useState<string>('Asphalt Charcoal');

  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Sync dark mode class on document
  useEffect(() => {
    const root = document.documentElement;
    if (darkMode) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [darkMode]);

  // Persist cart
  useEffect(() => {
    try {
      localStorage.setItem('hoodoo_cart', JSON.stringify(cart));
    } catch (e) {
      // ignore
    }
  }, [cart]);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3500);
  };

  const handleAddToCart = (product: Product, size: string, color: string) => {
    setCart((prev) => {
      const idx = prev.findIndex(
        (ci) =>
          ci.product.id === product.id &&
          ci.selectedSize === size &&
          ci.selectedColor === color
      );
      if (idx > -1) {
        const copy = [...prev];
        copy[idx].quantity += 1;
        return copy;
      }
      return [
        ...prev,
        {
          product,
          selectedSize: size,
          selectedColor: color,
          quantity: 1,
        },
      ];
    });
    showToast(`Added ${product.name} (${size}) to Bag`);
  };

  const handleQuickAdd = (product: Product) => {
    const defaultColor = product.swatches?.[0]?.name || 'Standard';
    const defaultSize = product.sizes?.[0] || 'L';
    handleAddToCart(product, defaultSize, defaultColor);
  };

  const handleDirectBuy = (product: Product, size: string, color: string) => {
    handleAddToCart(product, size, color);
    setIsCartOpen(false);
    setIsCheckoutOpen(true);
  };

  const handleUpdateQuantity = (index: number, newQty: number) => {
    setCart((prev) => {
      if (newQty <= 0) {
        return prev.filter((_, i) => i !== index);
      }
      const copy = [...prev];
      copy[index].quantity = newQty;
      return copy;
    });
  };

  const handleRemoveItem = (index: number) => {
    setCart((prev) => prev.filter((_, i) => i !== index));
  };

  const handleOpen3D = (product?: Product, color?: string) => {
    const targetProduct = product || currentHeroProduct;
    const targetColor = color || targetProduct.swatches?.[0]?.name || 'Standard';
    setStudioProduct(targetProduct);
    setStudioColor(targetColor);
    setIs3DModalOpen(true);
  };

  const totalCartCount = cart.reduce((acc, item) => acc + item.quantity, 0);

  return (
    <div className="min-h-screen flex flex-col bg-[#f5f5f4] dark:bg-[#0a0a0c] text-neutral-900 dark:text-neutral-100 transition-colors duration-200">
      {/* Skip to Main Content Landmark for A11y */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-neutral-950 focus:text-white focus:dark:bg-white focus:dark:text-neutral-950 focus:rounded-md focus:shadow-xl focus:font-mono focus:text-xs focus:font-bold focus:outline-none focus:ring-2 focus:ring-neutral-400"
      >
        Skip to main content
      </a>

      {/* Top Header */}
      <Header
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        cartCount={totalCartCount}
        onOpenCart={() => setIsCartOpen(true)}
        currentPage={currentPage}
        onNavigate={(page) => {
          setCurrentPage(page);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
        onOpen3D={() => handleOpen3D()}
        palette={palette}
        onSelectPalette={setPalette}
      />

      {/* Main Content Router */}
      <main id="main-content" className="flex-1" tabIndex={-1}>
        {currentPage === 'home' && (
          <>
            <HeroSpotlight
              currentProduct={currentHeroProduct}
              setCurrentProduct={setCurrentHeroProduct}
              onAddToCart={handleAddToCart}
              onDirectBuy={handleDirectBuy}
              onOpen3D={(p, c) => handleOpen3D(p, c)}
              palette={palette}
            />
            <CatalogGrid
              activeSpotlightId={currentHeroProduct.id}
              onSelectProduct={(p) => {
                setCurrentHeroProduct(p);
                window.scrollTo({ top: 100, behavior: 'smooth' });
              }}
              onQuickAdd={handleQuickAdd}
              onOpen3D={(p) => handleOpen3D(p)}
              palette={palette}
            />
          </>
        )}

        {currentPage === 'about' && (
          <AboutPage onBackToCatalog={() => setCurrentPage('home')} />
        )}

        {currentPage === 'policy' && (
          <PolicyPage
            onBackToCatalog={() => setCurrentPage('home')}
            onNavigateToCookiePolicy={() => setCurrentPage('cookie-policy')}
          />
        )}

        {currentPage === 'cookie-policy' && (
          <CookiePolicyPage onBackToCatalog={() => setCurrentPage('home')} />
        )}
      </main>

      {/* Footer */}
      <Footer
        onNavigate={(page) => {
          setCurrentPage(page);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
        palette={palette}
      />

      {/* Slide-over Cart Drawer */}
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

      {/* Checkout Modal */}
      <CheckoutModal
        isOpen={isCheckoutOpen}
        onClose={() => setIsCheckoutOpen(false)}
        cartItems={cart}
        onOrderComplete={() => {
          setCart([]);
          showToast('Order confirmed! Check your email.');
        }}
      />

      {/* Real-Time Three.js 3D Studio Modal */}
      <ThreeDStudioModal
        isOpen={is3DModalOpen}
        onClose={() => setIs3DModalOpen(false)}
        initialProduct={studioProduct}
        initialColor={studioColor}
        palette={palette}
      />

      {/* Cookie Consent Notice */}
      <CookieBanner onNavigateToCookiePolicy={() => setCurrentPage('cookie-policy')} />

      {/* Action Notification Toast */}
      <Toast message={toastMessage} onOpenCart={() => setIsCartOpen(true)} />
    </div>
  );
}
export default App;
