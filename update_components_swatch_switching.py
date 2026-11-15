import os

hero_spotlight_code = '''import React, { useState, useEffect } from 'react';
import type { Product } from '../types';
import { THUMBNAIL_PRODUCTS } from '../data/products';

interface HeroSpotlightProps {
  currentProduct: Product;
  setCurrentProduct: (p: Product) => void;
  onAddToCart: (product: Product, size: string, color: string) => void;
  onDirectBuy: (product: Product, size: string, color: string) => void;
}

export const HeroSpotlight: React.FC<HeroSpotlightProps> = ({
  currentProduct,
  setCurrentProduct,
  onAddToCart,
  onDirectBuy,
}) => {
  const [selectedSize, setSelectedSize] = useState<string>('L');
  const [selectedColor, setSelectedColor] = useState<string>(
    currentProduct.swatches?.[0]?.name || 'Standard'
  );
  const [displayImage, setDisplayImage] = useState<string>(currentProduct.image);

  // Sync display image when currentProduct changes
  useEffect(() => {
    const defaultSwatch = currentProduct.swatches?.[0];
    setSelectedColor(defaultSwatch?.name || 'Standard');
    setDisplayImage(defaultSwatch?.image || currentProduct.image);
  }, [currentProduct.id]);

  const handleSelectColorway = (swatchName: string, swatchImage?: string) => {
    setSelectedColor(swatchName);
    if (swatchImage) {
      setDisplayImage(swatchImage);
    }
  };

  return (
    <div className="flex flex-col justify-between h-full bg-transparent p-4 sm:p-6 lg:p-8">
      {/* Top Main Spotlight Section */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-8 lg:gap-10 items-center">
        
        {/* Left: Product Showcase with Soft Grey Studio Backlight */}
        <div className="md:col-span-6 flex flex-col items-center justify-center relative">
          <div className="w-full max-w-[420px] aspect-square flex items-center justify-center relative product-image-container">
            
            {/* The Neutral Grey Studio Backlight: Keeps black garments popping on black & white on white */}
            <div className="absolute inset-0 rounded-full product-backlight blur-2xl pointer-events-none scale-115 opacity-80" />

            {/* Product Image: Clean transparent background */}
            <img
              key={displayImage}
              src={displayImage}
              alt={currentProduct.name}
              className="max-h-[340px] w-auto object-contain relative z-10 drop-shadow-[0_16px_32px_rgba(0,0,0,0.3)] transition-transform duration-300 hover:scale-105 animate-fadeIn"
            />
          </div>
        </div>

        {/* Right: Product Narrative, Sizing, and Action Buttons */}
        <div className="md:col-span-6 flex flex-col justify-center space-y-6">
          <div>
            <div className="text-[11px] font-bold tracking-widest text-neutral-400 uppercase font-mono">
              WEST COAST DROP • 500GSM
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight uppercase leading-[1.05] font-display text-neutral-950 dark:text-neutral-50 mt-1">
              {currentProduct.name}
            </h1>
            {currentProduct.quote && (
              <p className="text-sm sm:text-base italic text-neutral-500 dark:text-neutral-400 font-serif mt-2 font-normal">
                {currentProduct.quote}
              </p>
            )}
            <p className="text-xs sm:text-sm text-neutral-700 dark:text-neutral-300 mt-2 leading-relaxed">
              {currentProduct.description}
            </p>
          </div>

          {/* Colorway Swatches with Live Photo Switching */}
          {currentProduct.swatches && currentProduct.swatches.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-[11px] font-bold tracking-wider text-neutral-400 uppercase font-mono">
                <span>OFFERED COLORWAY:</span>
                <span className="text-neutral-950 dark:text-white font-bold">{selectedColor}</span>
              </div>
              <div className="flex items-center gap-3">
                {currentProduct.swatches.map((swatch) => (
                  <button
                    key={swatch.name}
                    onClick={() => handleSelectColorway(swatch.name, swatch.image)}
                    className={`relative p-1 rounded-full transition-all ${
                      selectedColor === swatch.name
                        ? 'ring-2 ring-neutral-950 dark:ring-white scale-110 shadow-sm'
                        : 'opacity-55 hover:opacity-100'
                    }`}
                    title={swatch.name}
                  >
                    <div
                      className="w-6 h-6 rounded-full border border-neutral-300 dark:border-neutral-700 shadow-inner"
                      style={{ backgroundColor: swatch.color }}
                    />
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Sizing Selector */}
          <div className="space-y-2">
            <span className="text-[11px] font-bold tracking-wider text-neutral-400 uppercase block font-mono">
              BOX-CUT SIZING
            </span>
            <div className="flex flex-wrap gap-2">
              {currentProduct.sizes.map((size) => (
                <button
                  key={size}
                  onClick={() => setSelectedSize(size)}
                  className={`h-9 px-4 rounded-lg text-xs font-bold tracking-wider transition-all font-mono ${
                    selectedSize === size
                      ? 'bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 shadow-sm'
                      : 'bg-neutral-200/60 dark:bg-neutral-800/60 text-neutral-800 dark:text-neutral-200 hover:bg-neutral-300 dark:hover:bg-neutral-700'
                  }`}
                >
                  {size}
                </button>
              ))}
            </div>
          </div>

          {/* Price & Action Buttons */}
          <div className="pt-2 space-y-4">
            <div className="text-3xl sm:text-4xl font-black tracking-tight font-display text-neutral-950 dark:text-white">
              ${currentProduct.price}
            </div>

            {/* CTAs */}
            <div className="flex items-center gap-4 max-w-md">
              <button
                onClick={() => onDirectBuy(currentProduct, selectedSize, selectedColor)}
                className="flex-1 py-4 px-6 bg-neutral-950 hover:bg-black text-white dark:bg-white dark:text-neutral-950 dark:hover:bg-neutral-200 rounded-xl font-extrabold text-xs tracking-widest uppercase transition-all active:translate-y-[1px] text-center"
              >
                BUY NOW
              </button>
              <button
                onClick={() => onAddToCart(currentProduct, selectedSize, selectedColor)}
                className="flex-1 py-4 px-6 bg-neutral-800 hover:bg-neutral-900 text-white dark:bg-neutral-200 dark:text-neutral-950 dark:hover:bg-neutral-300 rounded-xl font-extrabold text-xs tracking-widest uppercase transition-all active:translate-y-[1px] text-center"
              >
                ADD TO CART
              </button>
            </div>
          </div>

        </div>

      </div>

      {/* Bottom Sub-Thumbnails: Archive vault row */}
      <div className="mt-12 pt-6">
        <div className="flex items-center justify-between mb-4">
          <span className="text-[11px] font-bold tracking-widest text-neutral-400 uppercase font-mono">
            STREET ARCHIVE VAULT
          </span>
          <span className="text-[10px] text-neutral-400 uppercase tracking-wider font-mono">
            TAP TO SPOTLIGHT
          </span>
        </div>

        <div className="grid grid-cols-3 gap-4">
          {THUMBNAIL_PRODUCTS.map((thumb) => {
            const isSelected = currentProduct.id === thumb.id;
            return (
              <button
                key={thumb.id}
                onClick={() => setCurrentProduct(thumb)}
                className={`p-3 rounded-2xl flex flex-col items-center justify-center transition-all relative product-image-container ${
                  isSelected
                    ? 'bg-neutral-200/80 dark:bg-neutral-800/80 ring-1 ring-neutral-400 dark:ring-neutral-600'
                    : 'bg-neutral-100/50 dark:bg-neutral-900/40 hover:bg-neutral-200/50 dark:hover:bg-neutral-800/40'
                }`}
              >
                <div className="absolute inset-0 rounded-2xl product-backlight opacity-60 pointer-events-none" />
                <img
                  src={thumb.image}
                  alt={thumb.name}
                  className="h-16 sm:h-20 w-auto object-contain relative z-10 transition-transform duration-300 drop-shadow-sm"
                />
                <span className="mt-2 text-[11px] font-bold text-neutral-800 dark:text-neutral-200 relative z-10">
                  ${thumb.price}
                </span>
              </button>
            );
          })}
        </div>
      </div>

    </div>
  );
};
'''
with open('src/components/HeroSpotlight.tsx', 'w', encoding='utf-8') as f:
    f.write(hero_spotlight_code)

catalog_grid_code = '''import React, { useState } from 'react';
import type { Product } from '../types';
import { CATALOG_PRODUCTS } from '../data/products';
import { Search, Plus, Check } from 'lucide-react';

interface CatalogGridProps {
  onSelectProduct: (product: Product) => void;
  onQuickAdd: (product: Product) => void;
  activeSpotlightId: string;
}

export const CatalogGrid: React.FC<CatalogGridProps> = ({
  onSelectProduct,
  onQuickAdd,
  activeSpotlightId,
}) => {
  const [filter, setFilter] = useState<'all' | 'hoodie' | 'tee' | 'kicks'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [addedId, setAddedId] = useState<string | null>(null);
  const [selectedColorwayMap, setSelectedColorwayMap] = useState<Record<string, { name: string; image: string }>>({});

  const filteredProducts = CATALOG_PRODUCTS.filter((product) => {
    const matchesFilter = filter === 'all' || product.category === filter;
    const matchesSearch =
      product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      product.subtitle?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const handleQuickAddClick = (e: React.MouseEvent, product: Product) => {
    e.stopPropagation();
    onQuickAdd(product);
    setAddedId(product.id);
    setTimeout(() => setAddedId(null), 1200);
  };

  const handleSelectColorway = (e: React.MouseEvent, productId: string, name: string, image: string) => {
    e.stopPropagation();
    setSelectedColorwayMap((prev) => ({
      ...prev,
      [productId]: { name, image },
    }));
  };

  return (
    <div id="catalog-section" className="flex flex-col h-full bg-transparent p-4 sm:p-6 lg:p-8">
      {/* Top Filter Tabs & Search */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-8">
        
        {/* Category Filter Tabs */}
        <div className="flex items-center gap-6 overflow-x-auto pb-1 sm:pb-0 scrollbar-none text-xs font-bold tracking-wider uppercase font-mono">
          {[
            { id: 'all', label: 'ALL GEAR' },
            { id: 'hoodie', label: 'HEAVY HOODIES' },
            { id: 'tee', label: 'BOXY TEES' },
            { id: 'kicks', label: 'KICKS' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setFilter(tab.id as any)}
              className={`transition-colors py-1 relative ${
                filter === tab.id
                  ? 'text-neutral-950 dark:text-white font-extrabold'
                  : 'text-neutral-500 dark:text-neutral-400 hover:text-neutral-950 dark:hover:text-white'
              }`}
            >
              {tab.label}
              {filter === tab.id && (
                <span className="absolute -bottom-1 left-0 right-0 h-[2px] bg-neutral-950 dark:bg-white rounded-full" />
              )}
            </button>
          ))}
        </div>

        {/* Minimal Search Input */}
        <div className="relative min-w-[220px]">
          <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" />
          <input
            type="text"
            placeholder="Search drop or cut..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-2 rounded-full text-xs bg-neutral-200/50 dark:bg-neutral-800/50 outline-none text-neutral-900 dark:text-neutral-100 placeholder:text-neutral-400 focus:ring-1 focus:ring-neutral-400 dark:focus:ring-neutral-600 transition-colors"
          />
        </div>

      </div>

      {/* 4-Column Grid: Clean, borderless cards with soft grey backlights */}
      <div className="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-4 gap-6 sm:gap-8">
        {filteredProducts.map((product) => {
          const isSelected = activeSpotlightId === product.id;
          const isJustAdded = addedId === product.id;
          const activeImage = selectedColorwayMap[product.id]?.image || product.image;

          return (
            <div
              key={product.id}
              onClick={() => onSelectProduct(product)}
              className={`group flex flex-col items-center justify-between p-4 rounded-2xl cursor-pointer transition-all duration-300 relative ${
                isSelected
                  ? 'bg-neutral-200/60 dark:bg-neutral-800/60 ring-1 ring-neutral-400 dark:ring-neutral-600'
                  : 'hover:bg-neutral-100/70 dark:hover:bg-neutral-900/50'
              }`}
            >
              {/* Product Visual Container with Soft Grey Backlight */}
              <div className="w-full aspect-square flex items-center justify-center relative my-2 product-image-container">
                
                {/* The Soft Grey Studio Backlight */}
                <div className="absolute inset-2 rounded-full product-backlight opacity-75 group-hover:opacity-100 transition-opacity pointer-events-none" />

                <img
                  key={activeImage}
                  src={activeImage}
                  alt={product.name}
                  loading="lazy"
                  className="max-h-28 sm:max-h-32 lg:max-h-36 w-auto object-contain relative z-10 drop-shadow-[0_8px_18px_rgba(0,0,0,0.22)] transition-transform duration-300 group-hover:scale-105"
                />

                {/* Quick Add Button */}
                <button
                  onClick={(e) => handleQuickAddClick(e, product)}
                  title="Quick Add to Bag"
                  className="absolute bottom-2 right-2 z-20 p-2 rounded-full bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 opacity-0 group-hover:opacity-100 transition-all hover:scale-110 active:scale-95 shadow-sm"
                >
                  {isJustAdded ? (
                    <Check className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <Plus className="w-3.5 h-3.5" />
                  )}
                </button>
              </div>

              {/* Colorway Swatches Preview on Card */}
              {product.swatches && (
                <div className="flex items-center gap-1.5 my-1.5 z-20">
                  {product.swatches.map((swatch) => {
                    const isSwatchActive = (selectedColorwayMap[product.id]?.name || product.swatches?.[0]?.name) === swatch.name;
                    return (
                      <button
                        key={swatch.name}
                        onClick={(e) => handleSelectColorway(e, product.id, swatch.name, swatch.image || product.image)}
                        className={`w-3.5 h-3.5 rounded-full border border-neutral-300 dark:border-neutral-700 transition-transform ${
                          isSwatchActive ? 'scale-125 ring-1 ring-neutral-950 dark:ring-white' : 'opacity-60 hover:opacity-100'
                        }`}
                        style={{ backgroundColor: swatch.color }}
                        title={swatch.name}
                      />
                    );
                  })}
                </div>
              )}

              {/* Product Metadata */}
              <div className="w-full text-center mt-2 space-y-1">
                <h3 className="text-xs font-bold text-neutral-900 dark:text-neutral-100 uppercase tracking-tight truncate font-sans">
                  {product.name}
                </h3>
                <p className="text-[11px] text-neutral-500 dark:text-neutral-400 truncate">
                  {product.subtitle}
                </p>
                <div className="text-xs font-extrabold text-neutral-900 dark:text-neutral-100 pt-1 font-mono">
                  ${product.price}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
'''
with open('src/components/CatalogGrid.tsx', 'w', encoding='utf-8') as f:
    f.write(catalog_grid_code)

print("Updated HeroSpotlight and CatalogGrid with dynamic colorway switching!")
