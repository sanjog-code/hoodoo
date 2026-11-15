import os

# Ensure directories exist
os.makedirs('src/components', exist_ok=True)
os.makedirs('src/pages', exist_ok=True)
os.makedirs('src/data', exist_ok=True)

# 1. src/data/products.ts
products_content = '''import { Product } from '../types';

export const FEATURED_HERO: Product = {
  id: 'wc-hero-hoodie',
  name: 'WESTSIDE LOWRIDER AIRBRUSH HOODIE',
  subtitle: 'Cut Raw & Oversized • 500GSM Iron Heavyweight',
  quote: '"If you weren\\'t raised on the block, don\\'t speak on it."',
  price: 195,
  category: 'hoodie',
  image: '/assets/westcoast_hero_hoodie.png',
  thumbnails: [
    '/assets/westcoast/wc_hoodie_01.png',
    '/assets/westcoast/wc_hoodie_02.png',
    '/assets/westcoast/wc_hoodie_03.png',
  ],
  swatches: [
    { name: 'Asphalt Charcoal', color: '#171717' },
    { name: 'Midnight Obsidian', color: '#09090b' },
    { name: 'Sun-Bleached Earth', color: '#443730' },
  ],
  description:
    'Heavy as concrete. We built this beast out of 500GSM brutal-weight fleece with zero polyester cheapness. Stamped with vintage lowrider murals, Old English hand-calligraphy, and paisley bandana accents across the sleeves. Boxy drop-shoulder cut that hangs stiff and mean over your belt.',
  fabricSpecs: [
    '500GSM Bulletproof Combed Fleece',
    'Custom West Coast Old English discharge screenprint',
    'Bandana paisley sleeve graphics',
    'Pre-shrunk pumice stone wash',
    'Double-needle raw reinforced hems',
  ],
  sizes: ['M', 'L', 'XL', 'XXL'],
  inStock: true,
  featured: true,
};

export const THUMBNAIL_PRODUCTS: Product[] = [
  {
    id: 'thumb-wc-01',
    name: 'WESTSIDE PAISLEY HOODIE',
    subtitle: 'Bandana Sleeves • Jet Black',
    price: 185,
    category: 'hoodie',
    image: '/assets/westcoast/wc_hoodie_01.png',
    description: 'Blacked-out boxy cut loaded with bandana paisley sleeves and crisp Old English script on the chest.',
    fabricSpecs: ['480GSM Heavyweight', 'Discharge Paisley Print', 'Deep Kangaroo Pouch'],
    sizes: ['M', 'L', 'XL', 'XXL'],
    inStock: true,
  },
  {
    id: 'thumb-wc-02',
    name: '\\'64 HYDRAULIC VINTAGE HOODIE',
    subtitle: 'Lowrider Pinstripe • Washed Cocoa',
    price: 175,
    category: 'hoodie',
    image: '/assets/westcoast/wc_hoodie_02.png',
    description: 'Faded earth wash with custom hood pinstriping pulled straight from a hydraulic-dipped \\'64 Impala.',
    fabricSpecs: ['460GSM Fleece', 'Mineral Earth Dye', 'Articulated Hood'],
    sizes: ['S', 'M', 'L', 'XL'],
    inStock: true,
  },
  {
    id: 'thumb-wc-03',
    name: 'COMPTON GOTHIC HEAVY HOODIE',
    subtitle: 'Midnight Blue • Chicano Lettering',
    price: 190,
    category: 'hoodie',
    image: '/assets/westcoast/wc_hoodie_03.png',
    description: 'Deep midnight hue with heavy blackletter chest embroidery. Stiff, boxy, and built to survive anything.',
    fabricSpecs: ['500GSM Heavyweight', 'High-density Ink', 'Tubular Construction'],
    sizes: ['M', 'L', 'XL'],
    inStock: true,
  },
];

export const CATALOG_PRODUCTS: Product[] = [
  {
    id: 'wc-cat-01',
    name: 'WESTSIDE PAISLEY HEAVY HOODIE',
    subtitle: 'Bandana Sleeves • 500GSM',
    price: 185,
    category: 'hoodie',
    image: '/assets/westcoast/wc_hoodie_01.png',
    description: 'You want real West Coast flavor? This is it. Heavyweight fleece, bandana paisley hits down both arms, and Old English script on the chest.',
    fabricSpecs: ['500GSM Heavy Cotton', 'Bandana Sleeve Panels', 'Oversized Boxy Fit'],
    sizes: ['M', 'L', 'XL', 'XXL'],
    inStock: true,
  },
  {
    id: 'wc-cat-02',
    name: '\\'64 LOWRIDER PINSTRIPE HOODIE',
    subtitle: 'Mineral Cocoa • Custom Airbrush',
    price: 175,
    category: 'hoodie',
    image: '/assets/westcoast/wc_hoodie_02.png',
    description: 'Inspired by weekend lowrider hops in Whittier Boulevard. Hand-distressed cocoa fleece with chrome pinstripes.',
    fabricSpecs: ['460GSM French Terry', 'Bleached Hem Detail', 'Pinstripe Discharge Print'],
    sizes: ['S', 'M', 'L', 'XL'],
    inStock: true,
  },
  {
    id: 'wc-cat-03',
    name: 'COMPTON BLACKLETTER HOODIE',
    subtitle: 'Midnight Charcoal • Raw Seams',
    price: 190,
    category: 'hoodie',
    image: '/assets/westcoast/wc_hoodie_03.png',
    description: 'Cold as the concrete curbs. Razor-sharp chicano gothic script with raw exposed flatlock stitching.',
    fabricSpecs: ['500GSM Unyielding Terry', 'Raw Cut Edges', 'Hidden Stash Pocket'],
    sizes: ['M', 'L', 'XL', 'XXL'],
    inStock: true,
  },
  {
    id: 'wc-cat-04',
    name: 'VENICE BOARDWALK CLAY HOODIE',
    subtitle: 'Sun-Bleached Sand • Boxy Cut',
    price: 180,
    category: 'hoodie',
    image: '/assets/westcoast/wc_hoodie_04.png',
    description: 'Looks and feels like it spent 10 years skating the Venice pit. Baked under the California sun with natural distress marks.',
    fabricSpecs: ['470GSM Organic Fleece', 'Sun-Fade Enzyme Wash', 'Thick Ribbed Hem'],
    sizes: ['S', 'M', 'L', 'XL'],
    inStock: true,
  },
  {
    id: 'wc-cat-05',
    name: 'CRENSHAW HEAVYWEIGHT BOXY TEE',
    subtitle: '280GSM Chalk White • Single-Stitch',
    price: 68,
    category: 'tee',
    image: '/assets/westcoast/wc_tee_01.png',
    description: 'Pure, unapologetic 90s boxy fit. Tight mock collar that never stretches out, thick 280GSM combed cotton, and Crenshaw block lettering.',
    fabricSpecs: ['280GSM Heavy Jersey', '1.25" Tight Rib Collar', 'Single-Stitch Construction'],
    sizes: ['S', 'M', 'L', 'XL', 'XXL'],
    inStock: true,
  },
  {
    id: 'wc-cat-06',
    name: 'SOUTH CENTRAL LOWRIDER TEE',
    subtitle: 'Washed Carbon • Pinstripe Print',
    price: 65,
    category: 'tee',
    image: '/assets/westcoast/wc_tee_02.png',
    description: 'Pumice-stoned carbon black with hand-drawn lowrider pinstripes. Slumps off the shoulders just the way you want.',
    fabricSpecs: ['270GSM Vintage Wash', 'Cracked Plastisol Ink', 'Seamless Body'],
    sizes: ['M', 'L', 'XL', 'XXL'],
    inStock: true,
  },
  {
    id: 'wc-cat-07',
    name: 'LOCALS ONLY CHICANO TEE',
    subtitle: 'Desert Sand • Gothic Cross',
    price: 64,
    category: 'tee',
    image: '/assets/westcoast/wc_tee_03.png',
    description: 'No tourists allowed. Raw sand tone with a bold Chicano cross and Old English hit. Wears in rugged.',
    fabricSpecs: ['260GSM Slub Cotton', 'Garment Pigment Wash', 'Dropped Shoulders'],
    sizes: ['S', 'M', 'L', 'XL'],
    inStock: true,
  },
  {
    id: 'wc-cat-08',
    name: 'EAST LA PAISLEY GRAPHIC TEE',
    subtitle: 'Indigo Washed • Bandana Motif',
    price: 72,
    category: 'tee',
    image: '/assets/westcoast/wc_tee_04.png',
    description: 'Deep indigo dye soaked in vinegar to lock that blue in. Stamped with authentic East LA bandana paisley details.',
    fabricSpecs: ['280GSM Ring-Spun Cotton', 'Vat-Dyed Indigo', 'Preshrunk'],
    sizes: ['M', 'L', 'XL', 'XXL'],
    inStock: true,
  },
  {
    id: 'wc-cat-09',
    name: 'STREET LOW \\'CHICANO BONE & GUM\\'',
    subtitle: 'Tumbled Leather • Raw Gum Sole',
    price: 215,
    category: 'kicks',
    image: '/assets/westcoast/wc_kick_01.png',
    description: 'Aged bone leather wrapped in bandana paisley accents on a sticky raw gum sole. Built to scrape pedals and kick skateboards.',
    fabricSpecs: ['Tumbled Full-Grain Leather', 'Bandana Print Overlays', 'Raw Gum Herringbone Sole'],
    sizes: ['US 8', 'US 9', 'US 10', 'US 11', 'US 12'],
    inStock: true,
  },
  {
    id: 'wc-cat-10',
    name: 'MIDNIGHT STEALTH RUNNER',
    subtitle: 'Triple Black • Thick Sole',
    price: 260,
    category: 'kicks',
    image: '/assets/westcoast/wc_kick_02.png',
    description: 'All-black shadow kicks for night runs. Sculpted chunky sole, reinforced toe box, zero shiny plastic.',
    fabricSpecs: ['Ballistic Mesh & Suede', 'Chunky EVA Midsole', 'Tonal Laces'],
    sizes: ['US 8.5', 'US 9.5', 'US 10', 'US 11'],
    inStock: true,
  },
  {
    id: 'wc-cat-11',
    name: 'CHOPPER SUEDE SKATE LOW',
    subtitle: 'Chocolate Suede • Fat Laces',
    price: 165,
    category: 'kicks',
    image: '/assets/westcoast/wc_kick_03.png',
    description: 'Throwback to Venice skate dogs. Thick hairy cow suede, fat laces, and reinforced ollie pads.',
    fabricSpecs: ['Heavy Duty Cow Suede', 'Fat Cotton Laces', 'Vulcanized Gum Outsole'],
    sizes: ['US 8', 'US 9', 'US 10', 'US 11'],
    inStock: true,
  },
  {
    id: 'wc-cat-12',
    name: 'PAISLEY SWOOP RETRO LOW',
    subtitle: 'Bone & Black • Bandana Tongue',
    price: 195,
    category: 'kicks',
    image: '/assets/westcoast/wc_kick_04.png',
    description: 'Classic court low retooled with bandana paisley quarter panels and aged cream midsoles.',
    fabricSpecs: ['Napa Leather Upper', 'Paisley Fabric Inset', 'Cushioned Footbed'],
    sizes: ['US 8', 'US 9', 'US 10', 'US 11'],
    inStock: true,
  },
  {
    id: 'wc-cat-13',
    name: 'MIDNIGHT RIDER GOTHIC HOODIE',
    subtitle: 'Asphalt Wash • 480GSM',
    price: 185,
    category: 'hoodie',
    image: '/assets/westcoast/wc_hoodie_05.png',
    description: 'Made for 2 AM freeway runs. Heavyweight stone-washed fleece, gothic backprint, and double-layer hood.',
    fabricSpecs: ['480GSM Fleece', 'Double-Layer Articulated Hood', 'Custom Ribbed Cuffs'],
    sizes: ['M', 'L', 'XL'],
    inStock: true,
  },
  {
    id: 'wc-cat-14',
    name: 'BLACKLETTER CHROME BOXY TEE',
    subtitle: 'Graphite Grey • Metallic Hit',
    price: 62,
    category: 'tee',
    image: '/assets/westcoast/wc_tee_05.png',
    description: 'Graphite boxy cut featuring raw metallic chrome script inspired by lowrider car badges.',
    fabricSpecs: ['260GSM Dense Jersey', 'Chrome Plastisol Print', 'Ribbed Collar'],
    sizes: ['S', 'M', 'L', 'XL'],
    inStock: true,
  },
  {
    id: 'wc-cat-15',
    name: 'CHICANO SOUL VINTAGE TEE',
    subtitle: 'Espresso Brown • Chicano Art',
    price: 64,
    category: 'tee',
    image: '/assets/westcoast/wc_tee_06.png',
    description: 'Rich dark espresso cotton faded with pumice stone. Stamped with vintage Chicano lowrider illustration.',
    fabricSpecs: ['270GSM Slub Cotton', 'Hand Distressed Edges', 'Oversized Fit'],
    sizes: ['S', 'M', 'L', 'XL'],
    inStock: true,
  },
  {
    id: 'wc-cat-16',
    name: 'EASTSIDE GUM SOLE RETRO',
    subtitle: 'Obsidian Black & Gum • Canvas',
    price: 205,
    category: 'kicks',
    image: '/assets/westcoast/wc_kick_05.png',
    description: 'Blacked-out heavy canvas and leather paired with pure raw gum rubber. Built for daily abuse.',
    fabricSpecs: ['16oz Canvas & Suede', 'Raw Gum Herringbone Sole', 'Steel Eyelets'],
    sizes: ['US 8', 'US 9', 'US 10', 'US 11', 'US 12'],
    inStock: true,
  },
];
'''
with open('src/data/products.ts', 'w', encoding='utf-8') as f:
    f.write(products_content)
print('Wrote src/data/products.ts')

# 2. src/components/Header.tsx
header_content = '''import React from 'react';
import { Moon, Sun, ShoppingBag } from 'lucide-react';

interface HeaderProps {
  darkMode: boolean;
  setDarkMode: (val: boolean | ((prev: boolean) => boolean)) => void;
  cartCount: number;
  onOpenCart: () => void;
  currentPage: 'home' | 'about' | 'policy' | 'cookie-policy';
  onNavigate: (page: 'home' | 'about' | 'policy' | 'cookie-policy') => void;
}

export const Header: React.FC<HeaderProps> = ({
  darkMode,
  setDarkMode,
  cartCount,
  onOpenCart,
  currentPage,
  onNavigate,
}) => {
  return (
    <header className="sticky top-0 z-40 w-full bg-[#f5f5f4]/90 dark:bg-[#0a0a0c]/90 backdrop-blur-md transition-colors border-b border-neutral-200/50 dark:border-neutral-800/40">
      <div className="max-w-[1600px] mx-auto px-6 lg:px-12 h-24 flex items-center justify-between">
        
        {/* Brand Logo: West Coast Old English Typography */}
        <button
          onClick={() => onNavigate('home')}
          className="flex items-center gap-3 transition-transform hover:opacity-90 active:scale-95"
          aria-label="HOODOO Home"
        >
          <img
            src="/assets/hoodoo_westcoast_logo.png"
            alt="HOODOO"
            className="h-10 sm:h-12 w-auto object-contain dark:invert"
          />
        </button>

        {/* Navigation & Controls */}
        <div className="flex items-center gap-8 sm:gap-12">
          <nav className="flex items-center gap-7 sm:gap-10 text-xs sm:text-sm font-bold tracking-wider uppercase font-sans">
            <button
              onClick={() => onNavigate('home')}
              className={`transition-colors py-1 relative ${
                currentPage === 'home'
                  ? 'text-neutral-950 dark:text-white font-extrabold'
                  : 'text-neutral-500 dark:text-neutral-400 hover:text-neutral-950 dark:hover:text-white'
              }`}
            >
              CATALOG
              {currentPage === 'home' && (
                <span className="absolute -bottom-1 left-0 right-0 h-[2px] bg-neutral-950 dark:bg-white rounded-full" />
              )}
            </button>

            <button
              onClick={() => onNavigate('about')}
              className={`transition-colors py-1 relative ${
                currentPage === 'about'
                  ? 'text-neutral-950 dark:text-white font-extrabold'
                  : 'text-neutral-500 dark:text-neutral-400 hover:text-neutral-950 dark:hover:text-white'
              }`}
            >
              ABOUT US
              {currentPage === 'about' && (
                <span className="absolute -bottom-1 left-0 right-0 h-[2px] bg-neutral-950 dark:bg-white rounded-full" />
              )}
            </button>

            <button
              onClick={() => onNavigate('policy')}
              className={`transition-colors py-1 relative ${
                currentPage === 'policy'
                  ? 'text-neutral-950 dark:text-white font-extrabold'
                  : 'text-neutral-500 dark:text-neutral-400 hover:text-neutral-950 dark:hover:text-white'
              }`}
            >
              POLICY
              {currentPage === 'policy' && (
                <span className="absolute -bottom-1 left-0 right-0 h-[2px] bg-neutral-950 dark:bg-white rounded-full" />
              )}
            </button>
          </nav>

          {/* Theme Toggle & Bag */}
          <div className="flex items-center gap-4 sm:gap-6">
            <button
              onClick={() => setDarkMode((prev) => !prev)}
              aria-label="Toggle Theme"
              className="p-2 text-neutral-600 dark:text-neutral-300 hover:text-neutral-950 dark:hover:text-white transition-colors"
            >
              {darkMode ? (
                <Sun className="w-5 h-5 transition-transform hover:rotate-45" />
              ) : (
                <Moon className="w-5 h-5 transition-transform hover:-rotate-12 fill-neutral-700" />
              )}
            </button>

            <button
              onClick={onOpenCart}
              aria-label="Open Shopping Bag"
              className="relative p-2 text-neutral-900 dark:text-neutral-100 hover:opacity-75 transition-opacity"
            >
              <ShoppingBag className="w-5 h-5 stroke-[2]" />
              {cartCount > 0 && (
                <span className="absolute -top-1 -right-2 min-w-[18px] h-[18px] px-1 bg-neutral-950 text-white dark:bg-white dark:text-black text-[10px] font-extrabold rounded-full flex items-center justify-center">
                  {cartCount}
                </span>
              )}
            </button>
          </div>
        </div>

      </div>
    </header>
  );
};
'''
with open('src/components/Header.tsx', 'w', encoding='utf-8') as f:
    f.write(header_content)
print('Wrote src/components/Header.tsx')

# 3. src/components/CatalogGrid.tsx
catalog_grid_content = '''import React, { useState } from 'react';
import { Product } from '../types';
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

  return (
    <div id="catalog-section" className="flex flex-col h-full bg-transparent p-4 sm:p-6 lg:p-8">
      {/* Top Filter Tabs & Search */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-8">
        
        {/* Category Filter Tabs */}
        <div className="flex items-center gap-6 overflow-x-auto pb-1 sm:pb-0 scrollbar-none text-xs font-bold tracking-wider uppercase">
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
                  src={product.image}
                  alt={product.name}
                  loading="lazy"
                  className="max-h-28 sm:max-h-32 lg:max-h-36 w-auto object-contain relative z-10 drop-shadow-[0_8px_18px_rgba(0,0,0,0.22)]"
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

              {/* Product Metadata */}
              <div className="w-full text-center mt-3 space-y-1">
                <h3 className="text-xs font-bold text-neutral-900 dark:text-neutral-100 uppercase tracking-tight truncate">
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
    f.write(catalog_grid_content)
print('Wrote src/components/CatalogGrid.tsx')

# 4. src/pages/AboutPage.tsx
about_content = '''import React from 'react';
import { ArrowLeft } from 'lucide-react';

interface AboutPageProps {
  onBackToCatalog: () => void;
}

export const AboutPage: React.FC<AboutPageProps> = ({ onBackToCatalog }) => {
  return (
    <div className="max-w-[1200px] mx-auto px-6 lg:px-12 py-12 lg:py-20 animate-fadeIn">
      {/* Return to Catalog */}
      <button
        onClick={onBackToCatalog}
        className="inline-flex items-center gap-2 text-xs font-bold tracking-wider text-neutral-500 hover:text-neutral-950 dark:hover:text-white uppercase transition-colors mb-12"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>BACK TO CATALOG</span>
      </button>

      {/* Main Editorial Hero */}
      <div className="space-y-6 max-w-3xl mb-16">
        <span className="text-xs font-extrabold tracking-widest text-neutral-400 uppercase font-mono">
          BORN IN LOS ANGELES • WEST COAST LORE
        </span>
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black uppercase tracking-tight font-display text-neutral-950 dark:text-white leading-[1.05]">
          BUILT FOR THE STREETS. ZERO FAST-FASHION BS.
        </h1>
        <p className="text-lg text-neutral-600 dark:text-neutral-300 font-serif italic">
          "If your hoodie collapses after three washes, it wasn\\'t made for the concrete."
        </p>
      </div>

      {/* Narrative Section */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-12 lg:gap-16 pt-8 border-t border-neutral-200/60 dark:border-neutral-800/60">
        
        <div className="md:col-span-5 space-y-4">
          <h2 className="text-xl font-black uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
            THE HOODOO DOCTRINE
          </h2>
          <p className="text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed">
            HOODOO was forged between Sunday lowrider hops down Whittier Boulevard and raw Venice skate pits. We were sick of corporate labels selling see-through poly-blend blanks with lazy graphics for $200.
          </p>
        </div>

        <div className="md:col-span-7 space-y-8 text-neutral-700 dark:text-neutral-300 text-sm sm:text-base leading-relaxed">
          <p>
            We mill our blanks at <strong>480GSM to 500GSM</strong>—thick enough to break the wind on a midnight freeway run and stiff enough to hold a true boxy street drape. No synthetic stretch. Just pure combed cotton that takes beatings, grease stains, and concrete scuffs, looking harder with every passing year.
          </p>
          <p>
            Our graphics pull straight from West Coast culture: hand-drawn Chicano blackletter calligraphy, lowrider hood pinstriping, and raw bandana paisley block cuts. Everything is screenprinted with heavy discharge ink that sinks directly into the cotton weave instead of sitting like cheap sticky plastic on top.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-6">
            <div className="space-y-2">
              <span className="text-2xl font-black font-display text-neutral-950 dark:text-white block">
                500 GSM
              </span>
              <h3 className="text-xs font-bold uppercase tracking-wider text-neutral-900 dark:text-neutral-100">
                Heavyweight Armor
              </h3>
              <p className="text-xs text-neutral-500">
                Bulletproof fleece weight that refuses to sag or wrinkle.
              </p>
            </div>

            <div className="space-y-2">
              <span className="text-2xl font-black font-display text-neutral-950 dark:text-white block">
                CHICANO
              </span>
              <h3 className="text-xs font-bold uppercase tracking-wider text-neutral-900 dark:text-neutral-100">
                Street Heritage
              </h3>
              <p className="text-xs text-neutral-500">
                Original Old English hand-lettering and authentic lowrider pinstripes.
              </p>
            </div>

            <div className="space-y-2">
              <span className="text-2xl font-black font-display text-neutral-950 dark:text-white block">
                RAW GUM
              </span>
              <h3 className="text-xs font-bold uppercase tracking-wider text-neutral-900 dark:text-neutral-100">
                Skate Cupsole
              </h3>
              <p className="text-xs text-neutral-500">
                Sticky raw gum outsoles engineered for daily street punishment.
              </p>
            </div>
          </div>
        </div>

      </div>

      {/* Return CTA */}
      <div className="mt-20 pt-10 border-t border-neutral-200/60 dark:border-neutral-800/60 flex justify-between items-center">
        <span className="text-xs text-neutral-400 uppercase tracking-widest font-mono">
          HOODOO LOS ANGELES // BRED ON THE WESTSIDE
        </span>
        <button
          onClick={onBackToCatalog}
          className="px-6 py-3 bg-neutral-950 hover:bg-black text-white dark:bg-white dark:text-neutral-950 dark:hover:bg-neutral-200 rounded-full text-xs font-extrabold uppercase tracking-wider transition-all"
        >
          EXPLORE GEAR
        </button>
      </div>
    </div>
  );
};
'''
with open('src/pages/AboutPage.tsx', 'w', encoding='utf-8') as f:
    f.write(about_content)
print('Wrote src/pages/AboutPage.tsx')

# 5. src/pages/PolicyPage.tsx
policy_content = '''import React from 'react';
import { ArrowLeft, Truck, RotateCcw, ShieldCheck, HeartHandshake } from 'lucide-react';

interface PolicyPageProps {
  onBackToCatalog: () => void;
  onNavigateToCookiePolicy: () => void;
}

export const PolicyPage: React.FC<PolicyPageProps> = ({
  onBackToCatalog,
  onNavigateToCookiePolicy,
}) => {
  return (
    <div className="max-w-[1200px] mx-auto px-6 lg:px-12 py-12 lg:py-20 animate-fadeIn">
      {/* Return to Catalog */}
      <button
        onClick={onBackToCatalog}
        className="inline-flex items-center gap-2 text-xs font-bold tracking-wider text-neutral-500 hover:text-neutral-950 dark:hover:text-white uppercase transition-colors mb-12"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>BACK TO CATALOG</span>
      </button>

      {/* Hero Header */}
      <div className="space-y-4 max-w-3xl mb-16">
        <span className="text-xs font-bold tracking-widest text-neutral-400 uppercase font-mono">
          CLIENT CARE & DISPATCH RULES
        </span>
        <h1 className="text-4xl sm:text-5xl font-black uppercase tracking-tight font-display text-neutral-950 dark:text-white leading-[1.1]">
          SHIPPING, EXCHANGES & CARE
        </h1>
        <p className="text-base text-neutral-600 dark:text-neutral-300">
          Straightforward policies. Zero runarounds. Tracked express dispatch on every single order.
        </p>
      </div>

      {/* Policy Details Grid */}
      <div className="space-y-12 divide-y divide-neutral-200/60 dark:divide-neutral-800/60">
        
        {/* Shipping */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4 flex items-center gap-3">
            <Truck className="w-5 h-5 text-neutral-950 dark:text-white" />
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              WORLDWIDE SHIPPING
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              Orders are boxed and dispatched within 24 to 48 business hours via DHL Express or FedEx Priority.
            </p>
            <ul className="list-disc list-inside space-y-1 text-neutral-500 dark:text-neutral-400 text-xs">
              <li>US Domestic Delivery: 2 to 4 business days.</li>
              <li>International Express: 3 to 6 business days with tracked door-to-door delivery.</li>
              <li>Free shipping is automatically applied on all orders exceeding $200.</li>
            </ul>
          </div>
        </div>

        {/* Returns & Exchanges */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4 flex items-center gap-3">
            <RotateCcw className="w-5 h-5 text-neutral-950 dark:text-white" />
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              14-DAY EXCHANGES
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              Got the wrong size? We offer exchanges or store credit within 14 calendar days of delivery as long as the garment is unwashed and in original condition.
            </p>
            <p className="text-xs text-neutral-500 dark:text-neutral-400">
              Email concierge at <span className="font-mono font-bold text-neutral-950 dark:text-white">support@hoodoo.studio</span> with your order number.
            </p>
          </div>
        </div>

        {/* Garment Care */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4 flex items-center gap-3">
            <HeartHandshake className="w-5 h-5 text-neutral-950 dark:text-white" />
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              500GSM GARMENT CARE
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              Our heavyweight fleece is nearly indestructible. Wash cold inside-out, hang dry to keep the heavyweight fibers tight and stiff.
            </p>
          </div>
        </div>

        {/* Privacy & Cookie Notice */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4 flex items-center gap-3">
            <ShieldCheck className="w-5 h-5 text-neutral-950 dark:text-white" />
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              PRIVACY & DATA
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              Payments are 256-bit encrypted. We never sell your personal information. Read our dedicated{' '}
              <button
                onClick={onNavigateToCookiePolicy}
                className="underline underline-offset-4 text-neutral-950 dark:text-white font-bold"
              >
                Cookie Policy
              </button>
              {' '}to learn how session storage is used.
            </p>
          </div>
        </div>

      </div>

      {/* Return CTA */}
      <div className="mt-20 pt-10 border-t border-neutral-200/60 dark:border-neutral-800/60 flex justify-between items-center">
        <span className="text-xs text-neutral-400 uppercase tracking-widest font-mono">
          QUESTIONS? CONCIERGE@HOODOO.STUDIO
        </span>
        <button
          onClick={onBackToCatalog}
          className="px-6 py-3 bg-neutral-950 hover:bg-black text-white dark:bg-white dark:text-neutral-950 dark:hover:bg-neutral-200 rounded-full text-xs font-extrabold uppercase tracking-wider transition-all"
        >
          RETURN TO CATALOG
        </button>
      </div>
    </div>
  );
};
'''
with open('src/pages/PolicyPage.tsx', 'w', encoding='utf-8') as f:
    f.write(policy_content)
print('Wrote src/pages/PolicyPage.tsx')

# 6. src/pages/CookiePolicyPage.tsx
cookie_content = '''import React from 'react';
import { ArrowLeft, Cookie } from 'lucide-react';

interface CookiePolicyPageProps {
  onBackToCatalog: () => void;
}

export const CookiePolicyPage: React.FC<CookiePolicyPageProps> = ({ onBackToCatalog }) => {
  return (
    <div className="max-w-[1200px] mx-auto px-6 lg:px-12 py-12 lg:py-20 animate-fadeIn">
      {/* Return to Catalog */}
      <button
        onClick={onBackToCatalog}
        className="inline-flex items-center gap-2 text-xs font-bold tracking-wider text-neutral-500 hover:text-neutral-950 dark:hover:text-white uppercase transition-colors mb-12"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>BACK TO CATALOG</span>
      </button>

      {/* Hero Header */}
      <div className="space-y-4 max-w-3xl mb-16">
        <span className="text-xs font-bold tracking-widest text-neutral-400 uppercase font-mono flex items-center gap-2">
          <Cookie className="w-4 h-4" />
          LEGAL & TRANSPARENCY
        </span>
        <h1 className="text-4xl sm:text-5xl font-black uppercase tracking-tight font-display text-neutral-950 dark:text-white leading-[1.1]">
          COOKIE POLICY
        </h1>
        <p className="text-base text-neutral-600 dark:text-neutral-300">
          Last updated: November 2026. This policy explains what cookies are, how HOODOO uses them, and how you can manage them in your browser.
        </p>
      </div>

      {/* Main Content Sections */}
      <div className="space-y-12 divide-y divide-neutral-200/60 dark:divide-neutral-800/60">
        
        {/* 1. What are cookies */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4">
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              1. WHAT ARE COOKIES?
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              Cookies are tiny text files placed on your device to ensure website features work correctly, remember what is in your shopping bag, and preserve your visual settings.
            </p>
          </div>
        </div>

        {/* 2. What cookies HOODOO uses */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4">
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              2. COOKIES WE USE
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-4">
            <div className="space-y-4">
              <div className="p-4 rounded-2xl bg-neutral-100/70 dark:bg-neutral-900/60 space-y-1">
                <div className="flex items-center justify-between font-mono text-xs font-bold text-neutral-900 dark:text-neutral-100">
                  <span>hoodoo_cart</span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-bold">Essential</span>
                </div>
                <p className="text-xs text-neutral-500">
                  Maintains your selected hoodies, sizes, and quantities in the bag across browsing sessions.
                </p>
                <div className="text-[10px] font-mono text-neutral-400">Duration: 30 days</div>
              </div>

              <div className="p-4 rounded-2xl bg-neutral-100/70 dark:bg-neutral-900/60 space-y-1">
                <div className="flex items-center justify-between font-mono text-xs font-bold text-neutral-900 dark:text-neutral-100">
                  <span>hoodoo_theme</span>
                  <span className="text-neutral-600 dark:text-neutral-300 font-bold">Preference</span>
                </div>
                <p className="text-xs text-neutral-500">
                  Saves your preference between Light Mode and Dark Mode.
                </p>
                <div className="text-[10px] font-mono text-neutral-400">Duration: 1 year</div>
              </div>

              <div className="p-4 rounded-2xl bg-neutral-100/70 dark:bg-neutral-900/60 space-y-1">
                <div className="flex items-center justify-between font-mono text-xs font-bold text-neutral-900 dark:text-neutral-100">
                  <span>session_telemetry</span>
                  <span className="text-neutral-600 dark:text-neutral-300 font-bold">Anonymous</span>
                </div>
                <p className="text-xs text-neutral-500">
                  Measures page loading performance without recording personal identity.
                </p>
                <div className="text-[10px] font-mono text-neutral-400">Duration: Session only</div>
              </div>
            </div>
          </div>
        </div>

        {/* 3. Managing Cookies */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pt-8">
          <div className="md:col-span-4">
            <h2 className="text-lg font-bold uppercase tracking-tight font-display text-neutral-900 dark:text-neutral-100">
              3. CONTROLLING COOKIES
            </h2>
          </div>
          <div className="md:col-span-8 text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed space-y-3">
            <p>
              You can inspect or delete cookies anytime in your browser settings under Privacy & Security (Chrome, Safari, Firefox, Edge).
            </p>
          </div>
        </div>

      </div>

      {/* Return CTA */}
      <div className="mt-20 pt-10 border-t border-neutral-200/60 dark:border-neutral-800/60 flex justify-between items-center">
        <span className="text-xs text-neutral-400 uppercase tracking-widest font-mono">
          LEGAL NOTICE // HOODOO
        </span>
        <button
          onClick={onBackToCatalog}
          className="px-6 py-3 bg-neutral-950 hover:bg-black text-white dark:bg-white dark:text-neutral-950 dark:hover:bg-neutral-200 rounded-full text-xs font-extrabold uppercase tracking-wider transition-all"
        >
          RETURN TO CATALOG
        </button>
      </div>
    </div>
  );
};
'''
with open('src/pages/CookiePolicyPage.tsx', 'w', encoding='utf-8') as f:
    f.write(cookie_content)
print('Wrote src/pages/CookiePolicyPage.tsx')

print('All sources constructed successfully!')
