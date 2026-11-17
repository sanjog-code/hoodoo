import React, { useState, useEffect, useMemo } from 'react';
import type { Product, Swatch } from '../types';
import { FEATURED_HERO, THUMBNAIL_PRODUCTS } from '../data/products';
import { RotateCw, Move3d, Sparkles, CheckCircle2 } from 'lucide-react';
import { BrandPalette, PALETTES } from './HoodooLogo';

interface HeroSpotlightProps {
  currentProduct: Product;
  setCurrentProduct: (p: Product) => void;
  onAddToCart: (product: Product, size: string, color: string) => void;
  onDirectBuy: (product: Product, size: string, color: string) => void;
  onOpen3D?: (product: Product, color: string) => void;
  palette?: BrandPalette;
}

export const HeroSpotlight: React.FC<HeroSpotlightProps> = ({
  currentProduct,
  setCurrentProduct,
  onAddToCart,
  onDirectBuy,
  onOpen3D,
  palette = 'cobalt',
}) => {
  const currentPalette = PALETTES[palette] || PALETTES.cobalt;
  const [selectedSize, setSelectedSize] = useState<string>('L');
  const [selectedColor, setSelectedColor] = useState<string>(
    currentProduct.swatches?.[0]?.name || 'Standard'
  );
  const [viewAngle, setViewAngle] = useState<'front' | 'back'>('front');

  // Sync state when currentProduct changes
  useEffect(() => {
    const defaultSwatch = currentProduct.swatches?.[0];
    setSelectedColor(defaultSwatch?.name || 'Standard');
    setViewAngle('front');

    // Instant Preloader: warm browser memory cache for all colorways of current piece
    currentProduct.swatches?.forEach((s) => {
      if (s.image) {
        const img = new Image();
        img.src = s.image;
      }
      if (s.backImage) {
        const img = new Image();
        img.src = s.backImage;
      }
    });
  }, [currentProduct.id]);

  // Determine active swatch and active image based on angle
  const activeSwatch: Swatch | undefined = currentProduct.swatches?.find(
    (s) => s.name === selectedColor
  ) || currentProduct.swatches?.[0];

  const frontImg = activeSwatch?.image || currentProduct.image;
  const backImg = activeSwatch?.backImage || currentProduct.backImage || frontImg.replace('.png', '_back.png');
  const displayImage = viewAngle === 'back' ? backImg : frontImg;

  const handleSelectColorway = (swatchName: string) => {
    setSelectedColor(swatchName);
  };

  const toggleViewAngle = () => {
    setViewAngle((prev) => (prev === 'front' ? 'back' : 'front'));
  };

  return (
    <div className="flex flex-col justify-between h-full bg-transparent p-4 sm:p-6 lg:p-8">
      {/* Top Main Spotlight Section */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-8 lg:gap-10 items-center">
        
        {/* Left: Product Showcase with Faint Grey Studio Backlight & Angle Switcher */}
        <div className="md:col-span-6 flex flex-col items-center justify-center relative">
          
          {/* Controls Bar: Angle Toggle + 3D View Space Action */}
          <div className="mb-3 flex flex-wrap items-center justify-center gap-2 z-20">
            <div className="flex items-center gap-1.5 p-1 bg-neutral-200/80 dark:bg-neutral-800/80 rounded-full border border-neutral-300/60 dark:border-neutral-700/60 backdrop-blur-sm">
              <button
                onClick={() => setViewAngle('front')}
                aria-pressed={viewAngle === 'front'}
                className={`px-3 py-1 text-[11px] font-mono font-bold tracking-wider rounded-full transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                  viewAngle === 'front'
                    ? 'bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 shadow-sm'
                    : 'text-neutral-700 dark:text-neutral-300 hover:text-neutral-950 dark:hover:text-white'
                }`}
                aria-label="Front View"
              >
                FRONT
              </button>
              <button
                onClick={() => setViewAngle('back')}
                aria-pressed={viewAngle === 'back'}
                className={`px-3 py-1 text-[11px] font-mono font-bold tracking-wider rounded-full transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                  viewAngle === 'back'
                    ? 'bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 shadow-sm'
                    : 'text-neutral-700 dark:text-neutral-300 hover:text-neutral-950 dark:hover:text-white'
                }`}
                aria-label="Back View"
              >
                BACK
              </button>
              <button
                onClick={toggleViewAngle}
                className="p-1 text-neutral-500 hover:text-neutral-950 dark:hover:text-white transition-transform hover:rotate-180 duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-full"
                aria-label="Flip Angle"
                title="Flip Angle"
              >
                <RotateCw className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Enter 3D View Space Button */}
            {onOpen3D && (
              <button
                onClick={() => onOpen3D(currentProduct, selectedColor)}
                className={`flex items-center gap-1.5 px-3.5 py-1.5 text-[11px] font-mono font-extrabold tracking-wider rounded-full ${currentPalette.buttonClass} shadow-sm transition-all active:scale-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400`}
                title="Open 3D Garment View"
                aria-label="Open 3D Studio"
              >
                <Move3d className="w-3.5 h-3.5" />
                <span>3D STUDIO</span>
              </button>
            )}
          </div>

          {/* Image Container with Studio Backlight */}
          <div className="relative w-full max-w-[420px] aspect-square flex items-center justify-center rounded-2xl overflow-hidden bg-neutral-100/60 dark:bg-neutral-900/60 border border-neutral-200/50 dark:border-neutral-800/50 shadow-sm">
            
            {/* Faint Grey Studio Backlight Glow */}
            <div
              className="absolute inset-0 pointer-events-none rounded-2xl"
              style={{
                background:
                  'radial-gradient(circle at center, rgba(160, 160, 160, 0.22) 0%, rgba(120, 120, 120, 0.08) 50%, transparent 75%)',
              }}
            />

            {/* Subtle Brand Accent Tint */}
            <div
              className="absolute inset-0 pointer-events-none opacity-20 transition-opacity duration-500"
              style={{
                background: `radial-gradient(circle at center, ${currentPalette.glow} 0%, transparent 70%)`,
              }}
            />

            {/* Product Rendering with Instant Swap & Zero DOM Thrashing */}
            <img
              src={displayImage}
              alt={`${currentProduct.name} - ${viewAngle.toUpperCase()} VIEW (${selectedColor})`}
              decoding="async"
              className="relative z-10 w-[90%] h-[90%] object-contain drop-shadow-[0_15px_25px_rgba(0,0,0,0.35)] transition-transform duration-300 hover:scale-105"
            />

            {/* Angle Badge */}
            <span className="absolute bottom-3 left-3 z-20 px-2 py-0.5 rounded text-[10px] font-mono font-bold tracking-widest bg-neutral-900/80 text-white dark:bg-white/90 dark:text-neutral-950 backdrop-blur-sm uppercase">
              {viewAngle} VIEW
            </span>
          </div>

        </div>

        {/* Right: Info, Price, Colorway Swatches, Sizing, and Direct Buy */}
        <div className="md:col-span-6 flex flex-col justify-center space-y-6">
          
          {/* Category & Badge */}
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-[10px] font-extrabold uppercase tracking-widest text-neutral-400 font-mono">
              ARCHIVE • {currentProduct.category}
            </span>
            <span className="text-neutral-600">•</span>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-neutral-900 border border-neutral-700/80 text-neutral-200">
              500GSM IRON FLEECE
            </span>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-neutral-900 border border-neutral-700/80 text-neutral-200">
              WEST COAST BOXY CUT
            </span>
          </div>

          {/* Product Title */}
          <div>
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black uppercase tracking-tight text-neutral-950 dark:text-white leading-[1.02] font-display">
              {currentProduct.name}
            </h1>
            {currentProduct.quote && (
              <p className="mt-1 text-xs text-neutral-700 dark:text-neutral-300 font-gothic tracking-wider italic">
                {currentProduct.quote}
              </p>
            )}
            <p className="mt-2 text-xs sm:text-sm text-neutral-700 dark:text-neutral-300 leading-relaxed max-w-lg font-sans">
              {currentProduct.description}
            </p>
            {currentProduct.fabricSpecs && currentProduct.fabricSpecs.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mt-3">
                {currentProduct.fabricSpecs.slice(0, 3).map((spec, i) => (
                  <span
                    key={i}
                    className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-md bg-neutral-900/90 border border-neutral-800 text-neutral-300"
                  >
                    {spec}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Colorway Swatches */}
          {currentProduct.swatches && currentProduct.swatches.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-[11px] uppercase tracking-wider font-mono text-neutral-700 dark:text-neutral-300">
                <span>OFFERED COLORWAY:</span>
                <span className="text-neutral-950 dark:text-white font-bold">{selectedColor}</span>
              </div>
              <div className="flex items-center gap-2" role="radiogroup" aria-label="Offered colorways">
                {currentProduct.swatches.map((swatch) => {
                  const isActive = selectedColor === swatch.name;
                  return (
                    <button
                      key={swatch.name}
                      onClick={() => handleSelectColorway(swatch.name)}
                      role="radio"
                      aria-checked={isActive}
                      className={`relative min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                        isActive
                          ? 'ring-2 ring-neutral-950 dark:ring-white scale-105 shadow-sm'
                          : 'opacity-70 hover:opacity-100'
                      }`}
                      aria-label={`Select colorway ${swatch.name}`}
                      title={swatch.name}
                    >
                      <div
                        className="w-7 h-7 rounded-full border border-neutral-300 dark:border-neutral-700 shadow-inner"
                        style={{ backgroundColor: swatch.color }}
                      />
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Sizing Selector */}
          <div className="space-y-2">
            <span className="text-[11px] font-bold tracking-wider text-neutral-700 dark:text-neutral-300 uppercase block font-mono">
              BOX-CUT SIZING
            </span>
            <div className="flex flex-wrap gap-2" role="radiogroup" aria-label="Garment sizes">
              {currentProduct.sizes.map((size) => (
                <button
                  key={size}
                  onClick={() => setSelectedSize(size)}
                  role="radio"
                  aria-checked={selectedSize === size}
                  className={`h-10 min-w-[44px] px-4 rounded-lg text-xs font-bold tracking-wider transition-all font-mono focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                    selectedSize === size
                      ? 'bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 shadow-sm'
                      : 'bg-neutral-200/80 dark:bg-neutral-800/80 text-neutral-800 dark:text-neutral-200 hover:bg-neutral-300 dark:hover:bg-neutral-700'
                  }`}
                  aria-label={`Select size ${size}`}
                >
                  {size}
                </button>
              ))}
            </div>
          </div>

          {/* Price & Action Buttons */}
          <div className="pt-2 space-y-4">
            <div className="flex items-baseline gap-3">
              <span className="text-3xl sm:text-4xl font-black tracking-tight font-display text-neutral-950 dark:text-white tabular-nums">
                ${currentProduct.price}
              </span>
              <span className="text-xs uppercase tracking-widest text-neutral-700 dark:text-neutral-300 font-mono font-medium">
                AVAILABLE · LA ATELIER DISPATCH
              </span>
            </div>

            {/* CTAs */}
            <div className="flex items-center gap-4 max-w-md">
              <button
                onClick={() => onDirectBuy(currentProduct, selectedSize, selectedColor)}
                className="flex-1 py-4 px-6 bg-neutral-950 hover:bg-black text-white dark:bg-white dark:text-neutral-950 dark:hover:bg-neutral-200 rounded-xl font-extrabold text-xs tracking-widest uppercase transition-all active:translate-y-[1px] text-center focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
                aria-label="Direct Buy Now"
              >
                BUY NOW
              </button>
              <button
                onClick={() => onAddToCart(currentProduct, selectedSize, selectedColor)}
                className={`flex-1 py-4 px-6 ${currentPalette.buttonClass} rounded-xl font-extrabold text-xs tracking-widest uppercase transition-all active:translate-y-[1px] text-center focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 shadow-sm`}
                aria-label="Add to Bag"
              >
                ADD TO CART
              </button>
            </div>
          </div>

        </div>

      </div>

      {/* Curated Capsule Collection: Interactive Archival Silhouette Switcher */}
      <div className="mt-12 pt-8 border-t border-neutral-200/80 dark:border-neutral-800/80">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2 mb-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-[11px] font-bold tracking-widest text-neutral-700 dark:text-neutral-300 uppercase font-mono">
                ARCHIVAL COLLECTION • 4 ICONIC SILHOUETTES
              </span>
            </div>
            <h3 className="text-base sm:text-lg font-black uppercase tracking-tight text-neutral-950 dark:text-white font-display">
              SELECT SILHOUETTE TO SPOTLIGHT ABOVE
            </h3>
          </div>
          <span className="text-xs font-mono text-neutral-600 dark:text-neutral-400">
            CLICK TO LOAD 3D MODEL & SPECS
          </span>
        </div>

        {/* 4 Rich Silhouette Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[FEATURED_HERO, ...THUMBNAIL_PRODUCTS].map((prod) => {
            const isSelected = prod.id === currentProduct.id;
            return (
              <button
                key={prod.id}
                onClick={() => setCurrentProduct(prod)}
                aria-pressed={isSelected}
                className={`group text-left p-3.5 rounded-2xl border transition-all duration-200 relative flex items-center gap-4 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                  isSelected
                    ? 'bg-white text-black border-white shadow-xl ring-2 ring-white'
                    : 'bg-white/40 dark:bg-neutral-900/40 text-neutral-900 dark:text-neutral-100 border-neutral-200/60 dark:border-neutral-800/60 hover:border-neutral-400 dark:hover:border-neutral-600 hover:bg-white dark:hover:bg-neutral-900/80'
                }`}
                aria-label={`Select ${prod.name}`}
              >
                {/* Product Thumbnail */}
                <div className={`relative w-16 h-16 sm:w-18 sm:h-18 flex-shrink-0 rounded-xl overflow-hidden p-1 flex items-center justify-center transition-colors ${
                  isSelected ? 'bg-neutral-100' : 'bg-neutral-200/50 dark:bg-neutral-800/50'
                }`}>
                  <img
                    src={prod.image}
                    alt={prod.name}
                    className="w-full h-full object-contain transition-opacity duration-200 group-hover:opacity-90 drop-shadow-sm"
                  />
                </div>

                {/* Product Metadata */}
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between gap-1 mb-0.5">
                    <span className={`text-[10px] font-mono font-bold tracking-widest uppercase ${
                      isSelected ? 'text-neutral-700' : 'text-neutral-600 dark:text-neutral-400'
                    }`}>
                      {prod.category}
                    </span>
                    <span className={`text-xs font-mono font-bold ${
                      isSelected ? 'text-black' : 'text-neutral-950 dark:text-white'
                    }`}>
                      ${prod.price}
                    </span>
                  </div>
                  <h4 className={`text-xs sm:text-[13px] font-bold uppercase tracking-tight truncate font-display ${
                    isSelected ? 'text-black' : 'text-neutral-950 dark:text-white'
                  }`}>
                    {prod.name}
                  </h4>
                  <div className="flex items-center gap-2 mt-1">
                    <span className={`text-[10px] font-mono font-medium ${
                      isSelected ? 'text-neutral-800' : 'text-neutral-600 dark:text-neutral-400'
                    }`}>
                      {prod.swatches?.length || 2} Colorways
                    </span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
