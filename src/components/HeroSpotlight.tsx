import React, { useState, useEffect } from 'react';
import type { Product, Swatch } from '../types';
import { THUMBNAIL_PRODUCTS } from '../data/products';
import { RotateCw, Move3d } from 'lucide-react';
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
                className={`px-3 py-1 text-[11px] font-mono font-bold tracking-wider rounded-full transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                  viewAngle === 'front'
                    ? 'bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 shadow-sm'
                    : 'text-neutral-600 dark:text-neutral-400 hover:text-neutral-950 dark:hover:text-white'
                }`}
                aria-label="Front View"
              >
                FRONT
              </button>
              <button
                onClick={() => setViewAngle('back')}
                className={`px-3 py-1 text-[11px] font-mono font-bold tracking-wider rounded-full transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                  viewAngle === 'back'
                    ? 'bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 shadow-sm'
                    : 'text-neutral-600 dark:text-neutral-400 hover:text-neutral-950 dark:hover:text-white'
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

            {/* Product Rendering */}
            <img
              key={displayImage}
              src={displayImage}
              alt={`${currentProduct.name} - ${viewAngle.toUpperCase()} VIEW (${selectedColor})`}
              className="relative z-10 w-[90%] h-[90%] object-contain drop-shadow-[0_15px_25px_rgba(0,0,0,0.35)] transition-transform duration-500 hover:scale-105"
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
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-bold uppercase tracking-widest text-neutral-500 dark:text-neutral-400 font-mono">
              DROP ARCHIVE · {currentProduct.category}
            </span>
            <span className="h-1 w-1 rounded-full bg-neutral-400" />
            <span className={`text-[10px] font-bold font-mono px-2 py-0.5 rounded-full ${currentPalette.subtleClass}`}>
              WEST COAST FIT
            </span>
          </div>

          {/* Product Title */}
          <div>
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black uppercase tracking-tight text-neutral-950 dark:text-white leading-[1.05] font-display">
              {currentProduct.name}
            </h1>
            <p className="mt-2 text-xs sm:text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed max-w-md">
              {currentProduct.description}
            </p>
          </div>

          {/* Colorway Swatches */}
          {currentProduct.swatches && currentProduct.swatches.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-[11px] uppercase tracking-wider font-mono text-neutral-500 dark:text-neutral-400">
                <span>OFFERED COLORWAY:</span>
                <span className="text-neutral-950 dark:text-white font-bold">{selectedColor}</span>
              </div>
              <div className="flex items-center gap-3">
                {currentProduct.swatches.map((swatch) => {
                  const isActive = selectedColor === swatch.name;
                  return (
                    <button
                      key={swatch.name}
                      onClick={() => handleSelectColorway(swatch.name)}
                      className={`relative p-1 rounded-full transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                        isActive
                          ? 'ring-2 ring-neutral-950 dark:ring-white scale-110 shadow-sm'
                          : 'opacity-65 hover:opacity-100'
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
            <span className="text-[11px] font-bold tracking-wider text-neutral-500 dark:text-neutral-400 uppercase block font-mono">
              BOX-CUT SIZING
            </span>
            <div className="flex flex-wrap gap-2">
              {currentProduct.sizes.map((size) => (
                <button
                  key={size}
                  onClick={() => setSelectedSize(size)}
                  className={`h-9 px-4 rounded-lg text-xs font-bold tracking-wider transition-all font-mono focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                    selectedSize === size
                      ? 'bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 shadow-sm'
                      : 'bg-neutral-200/60 dark:bg-neutral-800/60 text-neutral-800 dark:text-neutral-200 hover:bg-neutral-300 dark:hover:bg-neutral-700'
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
              <span className="text-xs uppercase tracking-widest text-neutral-600 dark:text-neutral-400 font-mono font-medium">
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

      {/* Bottom Sub-Thumbnails: Archive collection row */}
      <div className="mt-12 pt-6">
        <div className="flex items-center justify-between mb-4">
          <span className="text-[11px] font-bold tracking-widest text-neutral-500 dark:text-neutral-400 uppercase font-mono">
            ARCHIVE COLLECTION
          </span>
          <span className="text-[11px] font-mono text-neutral-400">
            SELECT PIECE
          </span>
        </div>
        <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-3">
          {THUMBNAIL_PRODUCTS.map((prod) => {
            const isSelected = prod.id === currentProduct.id;
            return (
              <button
                key={prod.id}
                onClick={() => setCurrentProduct(prod)}
                className={`group relative aspect-square rounded-xl p-1 bg-neutral-100 dark:bg-neutral-900 border transition-all overflow-hidden ${
                  isSelected
                    ? `${currentPalette.ringClass} ring-2 border-transparent scale-105 shadow-md`
                    : 'border-neutral-200 dark:border-neutral-800 opacity-70 hover:opacity-100 hover:border-neutral-400'
                }`}
                aria-label={`Select ${prod.name}`}
              >
                <img
                  src={prod.image}
                  alt={prod.name}
                  className="w-full h-full object-contain group-hover:scale-110 transition-transform duration-300"
                />
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
