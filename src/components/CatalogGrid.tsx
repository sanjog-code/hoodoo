import React, { useState, useMemo } from 'react';
import type { Product, Swatch } from '../types';
import { CATALOG_PRODUCTS } from '../data/products';
import { Search, Plus, Check, RotateCw, X, SlidersHorizontal, ArrowUpDown, Move3d } from 'lucide-react';
import { BrandPalette, PALETTES } from './HoodooLogo';

interface CatalogGridProps {
  onSelectProduct: (product: Product) => void;
  onQuickAdd: (product: Product) => void;
  activeSpotlightId: string;
  onOpen3D?: (product: Product) => void;
  palette?: BrandPalette;
}

type CategoryFilter = 'all' | 'hoodie' | 'tee' | 'kicks';
type ToneFilter = 'all' | 'dark' | 'light' | 'color';
type PriceFilter = 'all' | 'under100' | '100to180' | 'above180';
type SortOption = 'default' | 'price-asc' | 'price-desc' | 'name-asc';

export const CatalogGrid: React.FC<CatalogGridProps> = ({
  onSelectProduct,
  onQuickAdd,
  activeSpotlightId,
  onOpen3D,
  palette = 'cobalt',
}) => {
  const currentPalette = PALETTES[palette] || PALETTES.cobalt;
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>('all');
  const [toneFilter, setToneFilter] = useState<ToneFilter>('all');
  const [priceFilter, setPriceFilter] = useState<PriceFilter>('all');
  const [sortOption, setSortOption] = useState<SortOption>('default');
  const [searchQuery, setSearchQuery] = useState('');
  const [showFiltersPanel, setShowFiltersPanel] = useState(false);

  const [addedId, setAddedId] = useState<string | null>(null);
  const [selectedColorwayMap, setSelectedColorwayMap] = useState<
    Record<string, { name: string; image: string; backImage?: string }>
  >({});
  const [cardAngleMap, setCardAngleMap] = useState<Record<string, 'front' | 'back'>>({});

  // Filter & Sort Logic
  const filteredProducts = useMemo(() => {
    return CATALOG_PRODUCTS.filter((product) => {
      // Category match
      if (categoryFilter !== 'all' && product.category !== categoryFilter) {
        return false;
      }

      // Search match
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase().trim();
        const matchesName = product.name.toLowerCase().includes(query);
        const matchesSubtitle = (product.subtitle || '').toLowerCase().includes(query);
        const matchesDesc = product.description.toLowerCase().includes(query);
        const matchesSwatches = product.swatches?.some((s) =>
          s.name.toLowerCase().includes(query)
        );
        if (!matchesName && !matchesSubtitle && !matchesDesc && !matchesSwatches) {
          return false;
        }
      }

      // Tone match
      if (toneFilter !== 'all') {
        const hasMatchingTone = product.swatches?.some((s) => {
          const col = s.color.toLowerCase();
          const name = s.name.toLowerCase();
          const isDark =
            col === '#1c1917' ||
            col === '#111827' ||
            col === '#18181b' ||
            col === '#171717' ||
            name.includes('black') ||
            name.includes('charcoal') ||
            name.includes('asphalt') ||
            name.includes('noir');
          const isLight =
            col === '#f5f5f4' ||
            col === '#f8fafc' ||
            col === '#fafaf9' ||
            col === '#e2e8f0' ||
            name.includes('white') ||
            name.includes('bone') ||
            name.includes('raw') ||
            name.includes('cream');
          const isColor = !isDark && !isLight;

          if (toneFilter === 'dark') return isDark;
          if (toneFilter === 'light') return isLight;
          if (toneFilter === 'color') return isColor;
          return true;
        });
        if (!hasMatchingTone) return false;
      }

      // Price match
      if (priceFilter === 'under100' && product.price >= 100) return false;
      if (priceFilter === '100to180' && (product.price < 100 || product.price > 180)) return false;
      if (priceFilter === 'above180' && product.price <= 180) return false;

      return true;
    }).sort((a, b) => {
      if (sortOption === 'price-asc') return a.price - b.price;
      if (sortOption === 'price-desc') return b.price - a.price;
      if (sortOption === 'name-asc') return a.name.localeCompare(b.name);
      return 0;
    });
  }, [categoryFilter, searchQuery, toneFilter, priceFilter, sortOption]);

  const activeFiltersCount = useMemo(() => {
    let count = 0;
    if (categoryFilter !== 'all') count++;
    if (toneFilter !== 'all') count++;
    if (priceFilter !== 'all') count++;
    if (sortOption !== 'default') count++;
    if (searchQuery.trim()) count++;
    return count;
  }, [categoryFilter, toneFilter, priceFilter, sortOption, searchQuery]);

  const resetFilters = () => {
    setCategoryFilter('all');
    setToneFilter('all');
    setPriceFilter('all');
    setSortOption('default');
    setSearchQuery('');
  };

  const handleQuickAddClick = (e: React.MouseEvent, product: Product) => {
    e.stopPropagation();
    onQuickAdd(product);
    setAddedId(product.id);
    setTimeout(() => {
      setAddedId(null);
    }, 1500);
  };

  const handleSelectColorway = (
    e: React.MouseEvent,
    productId: string,
    swatch: Swatch
  ) => {
    e.stopPropagation();
    setSelectedColorwayMap((prev) => ({
      ...prev,
      [productId]: {
        name: swatch.name,
        image: swatch.image || '',
        backImage: swatch.backImage,
      },
    }));
  };

  const toggleCardAngle = (e: React.MouseEvent, productId: string) => {
    e.stopPropagation();
    setCardAngleMap((prev) => {
      const cur = prev[productId] || 'front';
      return {
        ...prev,
        [productId]: cur === 'front' ? 'back' : 'front',
      };
    });
  };

  return (
    <div className="space-y-6">
      
      {/* Controls Header: Category Tabs + Search + Secondary Filters Toggle */}
      <div className="space-y-4">
        
        {/* Row 1: Primary Category Tabs & Actions */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-neutral-200/80 dark:border-neutral-800/80 pb-4">
          
          {/* Category Tabs */}
          <div className="flex items-center gap-5 sm:gap-8 text-xs font-bold tracking-wider uppercase font-sans">
            {[
              { id: 'all', label: 'ALL GEAR' },
              { id: 'hoodie', label: 'HEAVY HOODIES' },
              { id: 'tee', label: 'BOXY TEES' },
              { id: 'kicks', label: 'KICKS' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setCategoryFilter(tab.id as CategoryFilter)}
                className={`transition-colors py-1 relative focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 rounded-sm ${
                  categoryFilter === tab.id
                    ? 'text-neutral-950 dark:text-white font-extrabold'
                    : 'text-neutral-600 dark:text-neutral-400 hover:text-neutral-950 dark:hover:text-white'
                }`}
                aria-label={`Filter by ${tab.label}`}
              >
                {tab.label}
                {categoryFilter === tab.id && (
                  <span className="absolute -bottom-1 left-0 right-0 h-[2px] bg-neutral-950 dark:bg-white rounded-full" />
                )}
              </button>
            ))}
          </div>

          {/* Search + Filter Toggle */}
          <div className="flex items-center gap-3">
            <div className="relative min-w-[200px] flex-1 sm:flex-initial">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" />
              <input
                type="text"
                placeholder="Search drop or cut..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-8 py-2 rounded-full text-xs bg-neutral-200/60 dark:bg-neutral-800/60 outline-none text-neutral-900 dark:text-neutral-100 placeholder:text-neutral-500 focus:ring-2 focus:ring-neutral-400 transition-colors font-mono"
                aria-label="Search catalog"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 p-0.5 text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-200"
                  aria-label="Clear search"
                >
                  <X className="w-3 h-3" />
                </button>
              )}
            </div>

            <button
              onClick={() => setShowFiltersPanel((prev) => !prev)}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-full text-xs font-mono font-bold tracking-wider transition-all border focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 ${
                showFiltersPanel || activeFiltersCount > 0
                  ? currentPalette.activeFilterClass
                  : 'bg-neutral-200/60 dark:bg-neutral-800/60 border-neutral-300/60 dark:border-neutral-700/60 text-neutral-700 dark:text-neutral-300 hover:text-neutral-950 dark:hover:text-white'
              }`}
              aria-label="Toggle Filter Options"
            >
              <SlidersHorizontal className="w-3.5 h-3.5" />
              <span>FILTERS</span>
              {activeFiltersCount > 0 && (
                <span className="w-4 h-4 rounded-full bg-white text-neutral-950 text-[10px] flex items-center justify-center font-bold">
                  {activeFiltersCount}
                </span>
              )}
            </button>
          </div>

        </div>

        {/* Row 2: Secondary Multi-Axis Filters Dropdown Drawer */}
        {showFiltersPanel && (
          <div className="p-4 rounded-2xl bg-neutral-100/90 dark:bg-neutral-900/90 border border-neutral-300/50 dark:border-neutral-800/60 space-y-4 animate-fadeIn">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              
              {/* Filter 1: Colorway Tone */}
              <div className="space-y-1.5">
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-neutral-500 block">
                  COLORWAY TONE
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {[
                    { id: 'all', label: 'All Tones' },
                    { id: 'dark', label: 'Stealth/Noir' },
                    { id: 'light', label: 'Bone/Raw' },
                    { id: 'color', label: 'Vibrant' },
                  ].map((t) => (
                    <button
                      key={t.id}
                      onClick={() => setToneFilter(t.id as ToneFilter)}
                      className={`px-2.5 py-1 rounded-lg text-xs font-mono transition-colors ${
                        toneFilter === t.id
                          ? 'bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 font-bold'
                          : 'bg-neutral-200/70 dark:bg-neutral-800/70 text-neutral-600 dark:text-neutral-400 hover:text-neutral-950 dark:hover:text-white'
                      }`}
                    >
                      {t.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Filter 2: Price Bracket */}
              <div className="space-y-1.5">
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-neutral-500 block">
                  PRICE BRACKET
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {[
                    { id: 'all', label: 'All Prices' },
                    { id: 'under100', label: '< $100' },
                    { id: '100to180', label: '$100 - $180' },
                    { id: 'above180', label: '> $180' },
                  ].map((p) => (
                    <button
                      key={p.id}
                      onClick={() => setPriceFilter(p.id as PriceFilter)}
                      className={`px-2.5 py-1 rounded-lg text-xs font-mono transition-colors ${
                        priceFilter === p.id
                          ? 'bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 font-bold'
                          : 'bg-neutral-200/70 dark:bg-neutral-800/70 text-neutral-600 dark:text-neutral-400 hover:text-neutral-950 dark:hover:text-white'
                      }`}
                    >
                      {p.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Filter 3: Sort By */}
              <div className="space-y-1.5">
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-neutral-500 block flex items-center gap-1">
                  <ArrowUpDown className="w-3 h-3" />
                  <span>SORT ARCHIVE</span>
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {[
                    { id: 'default', label: 'Curated' },
                    { id: 'price-asc', label: 'Price: Low' },
                    { id: 'price-desc', label: 'Price: High' },
                    { id: 'name-asc', label: 'Alphabetical' },
                  ].map((s) => (
                    <button
                      key={s.id}
                      onClick={() => setSortOption(s.id as SortOption)}
                      className={`px-2.5 py-1 rounded-lg text-xs font-mono transition-colors ${
                        sortOption === s.id
                          ? 'bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 font-bold'
                          : 'bg-neutral-200/70 dark:bg-neutral-800/70 text-neutral-600 dark:text-neutral-400 hover:text-neutral-950 dark:hover:text-white'
                      }`}
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>

            </div>

            {/* Active filters status bar & Reset button */}
            <div className="flex items-center justify-between pt-2 border-t border-neutral-200/60 dark:border-neutral-800/60 text-xs">
              <span className="text-neutral-500 font-mono">
                Showing {filteredProducts.length} pieces
              </span>
              {activeFiltersCount > 0 && (
                <button
                  onClick={resetFilters}
                  className={`${currentPalette.badgeText} hover:underline font-bold font-mono`}
                >
                  RESET ALL FILTERS
                </button>
              )}
            </div>
          </div>
        )}

      </div>

      {/* Nine-States #3: Zero-results Fallback State */}
      {filteredProducts.length === 0 ? (
        <div className="my-16 flex flex-col items-center justify-center text-center p-8 border border-dashed border-neutral-300 dark:border-neutral-800 rounded-3xl">
          <div className="w-14 h-14 rounded-full bg-neutral-200 dark:bg-neutral-800 flex items-center justify-center mb-4 text-neutral-400">
            <Search className="w-6 h-6" />
          </div>
          <h3 className="text-base font-extrabold uppercase font-mono tracking-tight text-neutral-900 dark:text-neutral-100">
            NO PIECES MATCH YOUR FILTER CRITERIA
          </h3>
          <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1 max-w-sm">
            Try broadening your search term, toggling other colorway tones, or resetting the filters.
          </p>
          <button
            onClick={resetFilters}
            className="mt-5 px-6 py-2.5 bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 font-mono text-xs font-bold uppercase rounded-full hover:opacity-90 transition-opacity focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
          >
            RESET ALL FILTERS
          </button>
        </div>
      ) : (
        /* 4-Column Grid: Borderless cards with soft grey backlights */
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
          {filteredProducts.map((product) => {
            const isSelected = product.id === activeSpotlightId;
            const isJustAdded = addedId === product.id;

            // Determine image from active colorway or angle
            const selectedCustomColor = selectedColorwayMap[product.id];
            const currentAngle = cardAngleMap[product.id] || 'front';

            let activeImage = selectedCustomColor?.image || product.image;
            if (currentAngle === 'back') {
              activeImage =
                selectedCustomColor?.backImage ||
                product.backImage ||
                activeImage.replace('.png', '_back.png');
            }

            return (
              <div
                key={product.id}
                onClick={() => onSelectProduct(product)}
                className={`group flex flex-col items-center justify-between p-4 rounded-2xl cursor-pointer transition-all duration-300 relative select-none ${
                  isSelected
                    ? `bg-neutral-200/80 dark:bg-neutral-800/80 ring-2 ${currentPalette.ringClass} shadow-lg`
                    : 'hover:bg-neutral-100/70 dark:hover:bg-neutral-900/50'
                }`}
                tabIndex={0}
                role="button"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    onSelectProduct(product);
                  }
                }}
                aria-label={`Select ${product.name}`}
              >
                {/* Product Visual Container with Soft Grey Studio Backlight */}
                <div className="w-full aspect-square flex items-center justify-center relative my-2 product-image-container">
                  
                  {/* The Soft Grey Studio Backlight: isolator behind black and white products */}
                  <div className="absolute inset-2 rounded-full product-backlight opacity-75 group-hover:opacity-100 transition-opacity pointer-events-none" />

                  <img
                    key={`${activeImage}-${currentAngle}`}
                    src={activeImage}
                    alt={`${product.name} - ${currentAngle} view`}
                    loading="lazy"
                    className="max-h-28 sm:max-h-32 lg:max-h-36 w-auto object-contain relative z-10 drop-shadow-[0_8px_20px_rgba(0,0,0,0.25)] transition-transform duration-300 group-hover:scale-105"
                  />

                  {/* 3D Model Explorer Pill */}
                  {product.model3d && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectProduct(product);
                        if (onOpen3D) onOpen3D(product);
                      }}
                      className={`absolute top-1 right-1 z-20 px-2 py-0.5 rounded-full ${currentPalette.pillTagClass} text-[9px] font-mono font-extrabold uppercase tracking-wider backdrop-blur-sm opacity-90 group-hover:opacity-100 transition-all hover:scale-105 flex items-center gap-1 shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400`}
                      title="Inspect piece in 3D WebGL Space"
                      aria-label={`Inspect ${product.name} in 3D`}
                    >
                      <Move3d className="w-2.5 h-2.5" />
                      <span>3D</span>
                    </button>
                  )}

                  {/* Front/Back View Flip Button */}
                  <button
                    onClick={(e) => toggleCardAngle(e, product.id)}
                    className="absolute top-1 left-1 z-20 px-2 py-0.5 rounded-full bg-neutral-900/80 dark:bg-neutral-100/80 text-white dark:text-neutral-950 text-[10px] font-mono font-bold uppercase tracking-wider backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
                    title={`Switch to ${currentAngle === 'front' ? 'Back' : 'Front'} View`}
                    aria-label={`Switch ${product.name} to ${currentAngle === 'front' ? 'back' : 'front'} view`}
                  >
                    <RotateCw className="w-2.5 h-2.5" />
                    <span>{currentAngle === 'front' ? 'BACK' : 'FRONT'}</span>
                  </button>

                  {/* Quick Add Button */}
                  <button
                    onClick={(e) => handleQuickAddClick(e, product)}
                    title="Quick Add to Bag"
                    aria-label={`Quick add ${product.name} to cart`}
                    className="absolute bottom-1 right-1 z-20 p-2 rounded-full bg-neutral-950 text-white dark:bg-white dark:text-neutral-950 opacity-0 group-hover:opacity-100 transition-all hover:scale-110 active:scale-95 shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
                  >
                    {isJustAdded ? (
                      <Check className="w-3.5 h-3.5 text-emerald-400" />
                    ) : (
                      <Plus className="w-3.5 h-3.5" />
                    )}
                  </button>
                </div>

                {/* Colorway Swatches Preview on Card with >=32px touch bounding area */}
                {product.swatches && (
                  <div className="flex items-center gap-1 my-1 z-20">
                    {product.swatches.map((swatch) => {
                      const isSwatchActive =
                        (selectedColorwayMap[product.id]?.name ||
                          product.swatches?.[0]?.name) === swatch.name;
                      return (
                        <button
                          key={swatch.name}
                          onClick={(e) => handleSelectColorway(e, product.id, swatch)}
                          className="p-1 rounded-full flex items-center justify-center transition-transform hover:scale-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
                          title={swatch.name}
                          aria-label={`Select colorway ${swatch.name} for ${product.name}`}
                        >
                          <div
                            className={`w-3.5 h-3.5 rounded-full border border-neutral-300 dark:border-neutral-700 transition-all ${
                              isSwatchActive
                                ? `scale-125 ring-1.5 ${currentPalette.ringClass} shadow-sm`
                                : 'opacity-70 hover:opacity-100'
                            }`}
                            style={{ backgroundColor: swatch.color }}
                          />
                        </button>
                      );
                    })}
                  </div>
                )}

                {/* Product Metadata: Price hidden unless clicked/selected! */}
                <div className="w-full text-center mt-2 space-y-1">
                  <h3 className="text-xs font-bold text-neutral-900 dark:text-neutral-100 uppercase tracking-tight truncate font-sans">
                    {product.name}
                  </h3>
                  <p className="text-[11px] text-neutral-500 dark:text-neutral-400 truncate">
                    {product.subtitle}
                  </p>

                  {/* PRICE DISPLAY: Visible ONLY when clicked / selected */}
                  <div className="pt-1 min-h-[22px] flex items-center justify-center font-mono">
                    {isSelected ? (
                      <span className={`text-xs font-black ${currentPalette.badgeText} font-mono tracking-tight animate-fadeIn tabular-nums`}>
                        ${product.price} USD
                      </span>
                    ) : (
                      <span className="text-[10px] font-semibold uppercase tracking-wider text-neutral-400 group-hover:text-neutral-950 dark:group-hover:text-white transition-colors">
                        SELECT PIECE
                      </span>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
