import React, { useState } from 'react';
import { Flame, Sparkles, Plus, Check, Zap, Info } from 'lucide-react';
import { ReactiveButton, sfx } from './ReactiveButton';

export interface MenuItem {
  id: string;
  name: string;
  tagline: string;
  price: number;
  category: 'burgers' | 'shakes' | 'sides';
  spicyLevel: number; // 0 to 5
  inspo: string;
  image: string;
  desc: string;
  ingredients: string[];
}

export const KRUNCH_ITEMS: MenuItem[] = [
  {
    id: 'cyber-smash',
    name: 'THE CYBER-SMASH 2077',
    tagline: 'NIGHT CITY MAILLARD PROTOCOL',
    price: 14.50,
    category: 'burgers',
    spicyLevel: 4,
    inspo: 'Inspired by Cyberpunk 2077 Street Food',
    image: 'https://images.unsplash.com/photo-1586190848861-99aa4a171e90?auto=format&fit=crop&w=800&q=80',
    desc: 'Two 3.5oz 44 Farms dry-aged patties smashed paper-thin on 475°F iron. Molten habanero-jack cheese, crispy charred Vidalia laces, black garlic aioli, and Martin’s potato bun.',
    ingredients: ['44 Farms Dry-Aged Beef', 'Habanero Jack', 'Crispy Vidalia Laces', 'Black Garlic Aioli'],
  },
  {
    id: 'spider-bite',
    name: 'SPIDER-BITE CHOPPED SMASH',
    tagline: 'BROOKLYN BODEGA MULTIVERSE EDITION',
    price: 13.50,
    category: 'burgers',
    spicyLevel: 3,
    inspo: 'Inspired by Spider-Verse Bodega Culture',
    image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80',
    desc: 'Lace-crusted chopped beef steak seasoned with Brooklyn bodega adobo, melted sharp white cheddar, crinkle-cut cucumber pickles, and hot chili-honey drip.',
    ingredients: ['Adobo Chopped Steak', 'Sharp White Cheddar', 'Crinkle Pickles', 'Hot Chili Honey'],
  },
  {
    id: 'arcane-hextech',
    name: 'ARCANE HEXTECH TRIPLE',
    tagline: 'OVERCHARGED 10.5 OZ BRUTE WEIGHT',
    price: 17.00,
    category: 'burgers',
    spicyLevel: 2,
    inspo: 'Inspired by Arcane: League of Legends',
    image: 'https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=800&q=80',
    desc: 'Three stacked smash patties (10.5oz), double Wisconsin aged cheddar, shallot bacon jam, charred scallion remoulade on a toasted brioche crown.',
    ingredients: ['Triple Angus Patties', 'Double Cheddar', 'Shallot Bacon Jam', 'Scallion Remoulade'],
  },
  {
    id: 'bikini-bottom',
    name: 'BIKINI BOTTOM SECRET FORMULA',
    tagline: 'CRISPY KELP TALLOW FORMULA',
    price: 11.00,
    category: 'burgers',
    spicyLevel: 1,
    inspo: 'The Legendary Underwater Formula',
    image: 'https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?auto=format&fit=crop&w=800&q=80',
    desc: 'Golden sear beef patty, American cheese, crispy cucumber pickles, vine-ripe heirloom tomato slice, yellow mustard, and secret tangy pink spread.',
    ingredients: ['Caramelized Beef', 'American Cheese', 'Crisp Cucumbers', 'Secret Pink Spread'],
  },
  {
    id: 'dragonfruit-shake',
    name: 'NEON DRAGONFRUIT SHAKE',
    tagline: 'ULTRAVIOLET CHURNED CUSTARD',
    price: 8.50,
    category: 'shakes',
    spicyLevel: 0,
    inspo: 'Tokyo Night Market Street Sweets',
    image: 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=800&q=80',
    desc: 'Whole Jersey dairy frozen custard hand-spun with fresh pink dragonfruit puree, Madagascar vanilla bean paste, and popping popping boba pearls.',
    ingredients: ['Whole Jersey Milk Custard', 'Dragonfruit Puree', 'Popping Boba', 'Malted Vanilla'],
  },
  {
    id: 'tallow-russets',
    name: 'TALLOW TWICE-CRISP RUSSETS',
    tagline: 'DOUBLE-FRIED IN SMOKED BEEF TALLOW',
    price: 5.50,
    category: 'sides',
    spicyLevel: 1,
    inspo: 'French Fry Supremacy Standard',
    image: 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=800&q=80',
    desc: 'Idaho Kennebec cut potatoes soaked in brine, blanched, and twice-fried in seasoned beef tallow. Dusted with smoked Maldon sea salt and garlic aioli.',
    ingredients: ['Kennebec Potatoes', 'Pure Beef Tallow', 'Smoked Maldon Salt', 'Garlic Aioli'],
  },
];

interface KrunchMenuProps {
  onAddToCart: (item: MenuItem, customization?: string) => void;
}

export const KrunchMenu: React.FC<KrunchMenuProps> = ({ onAddToCart }) => {
  const [activeCategory, setActiveCategory] = useState<'all' | 'burgers' | 'shakes' | 'sides'>('all');
  const [addedItemId, setAddedItemId] = useState<string | null>(null);

  const filteredItems = activeCategory === 'all'
    ? KRUNCH_ITEMS
    : KRUNCH_ITEMS.filter((item) => item.category === activeCategory);

  const handleAdd = (item: MenuItem) => {
    sfx.playCrunch();
    onAddToCart(item);
    setAddedItemId(item.id);
    setTimeout(() => setAddedItemId(null), 1500);
  };

  return (
    <section id="menu" className="w-full py-20 px-4 sm:px-8 bg-neutral-950 relative">
      
      {/* Background Neon Lighting */}
      <div className="absolute top-1/2 left-0 w-80 h-80 bg-red-600/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute top-1/3 right-0 w-80 h-80 bg-amber-500/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto relative z-10">
        
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 font-mono text-xs font-bold uppercase tracking-widest mb-3">
              <Zap className="w-3.5 h-3.5 fill-current" />
              <span>THE DAILY CHOMP DISPATCH // EDITION 4.0</span>
            </div>
            <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight text-white font-sans uppercase">
              FEED YOUR <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-yellow-300 to-lime-400">BIG MOUTH</span>
            </h2>
            <p className="text-neutral-400 text-sm sm:text-base mt-2 max-w-2xl">
              Engineered with 44 Farms pasture-raised Texas beef, twice-fried tallow crisps, and whole Jersey custard. Smashed over 475°F iron with zero shortcuts.
            </p>
          </div>

          {/* Category Filter Pills */}
          <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-neutral-800 md:border-b-0">
            {(['all', 'burgers', 'shakes', 'sides'] as const).map((cat) => (
              <button
                key={cat}
                onClick={() => {
                  setActiveCategory(cat);
                  sfx.playPop(900);
                }}
                className={`px-4 py-2 rounded-xl text-xs font-mono font-bold uppercase tracking-wider transition-all select-none whitespace-nowrap active:translate-y-[1px] ${
                  activeCategory === cat
                    ? 'bg-amber-500 text-neutral-950 shadow-lg shadow-amber-500/20'
                    : 'bg-neutral-900 border border-neutral-800 text-neutral-400 hover:text-white hover:border-neutral-700'
                }`}
              >
                {cat === 'all' ? 'FULL MENU' : cat}
              </button>
            ))}
          </div>
        </div>

        {/* Menu Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredItems.map((item) => {
            const isJustAdded = addedItemId === item.id;

            return (
              <div
                key={item.id}
                className="rounded-2xl bg-neutral-900/90 border-2 border-neutral-800/80 hover:border-amber-400/60 transition-all duration-300 overflow-hidden flex flex-col justify-between group shadow-xl hover:shadow-[0_12px_32px_rgba(245,158,11,0.15)] relative"
              >
                {/* Top Image & Inspo Badge */}
                <div className="relative h-56 w-full overflow-hidden bg-black">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-90 group-hover:opacity-100"
                  />
                  
                  {/* Gradients */}
                  <div className="absolute inset-0 bg-gradient-to-t from-neutral-900 via-transparent to-black/40" />

                  {/* Pop Culture Inspo Pill */}
                  <span className="absolute top-3 left-3 px-2.5 py-1 rounded-md bg-neutral-950/80 backdrop-blur-md border border-neutral-700 text-amber-300 font-mono text-[10px] font-bold uppercase tracking-wider">
                    {item.inspo}
                  </span>

                  {/* Spicy Telemetry */}
                  {item.spicyLevel > 0 && (
                    <div className="absolute top-3 right-3 px-2 py-1 rounded-md bg-red-600/90 text-white font-mono text-[10px] font-extrabold flex items-center gap-1 shadow-md">
                      <Flame className="w-3 h-3 fill-white" />
                      <span>SPICE: {item.spicyLevel}/5</span>
                    </div>
                  )}

                  {/* Price Tag */}
                  <div className="absolute bottom-3 right-3 px-3 py-1.5 rounded-lg bg-amber-500 text-neutral-950 font-mono text-sm font-black tabular-nums shadow-lg">
                    ${item.price.toFixed(2)}
                  </div>
                </div>

                {/* Card Body */}
                <div className="p-6 flex-1 flex flex-col justify-between">
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-[0.2em] text-neutral-400 font-bold mb-1">
                      {item.tagline}
                    </div>
                    <h3 className="font-sans font-black text-xl text-white tracking-tight group-hover:text-amber-400 transition-colors">
                      {item.name}
                    </h3>
                    <p className="text-neutral-400 text-xs sm:text-sm mt-2 leading-relaxed">
                      {item.desc}
                    </p>

                    {/* Ingredient Tag Pills */}
                    <div className="flex flex-wrap gap-1.5 mt-4">
                      {item.ingredients.map((ing, i) => (
                        <span
                          key={i}
                          className="px-2 py-0.5 rounded bg-neutral-800/80 border border-neutral-700/60 text-neutral-300 font-mono text-[10px]"
                        >
                          {ing}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Action Button */}
                  <div className="mt-6 pt-4 border-t border-neutral-800/80 flex items-center justify-between gap-3">
                    <span className="text-[11px] font-mono text-neutral-500">
                      MADE TO ORDER // ~10M
                    </span>

                    <button
                      onClick={() => handleAdd(item)}
                      className={`px-4 py-2.5 rounded-xl font-sans text-xs font-black uppercase tracking-wider transition-all flex items-center gap-1.5 active:translate-y-[2px] ${
                        isJustAdded
                          ? 'bg-emerald-500 text-neutral-950 shadow-md shadow-emerald-500/30'
                          : 'bg-amber-500 hover:bg-amber-400 text-neutral-950 shadow-md shadow-amber-500/20'
                      }`}
                    >
                      {isJustAdded ? (
                        <>
                          <Check className="w-3.5 h-3.5 stroke-[3]" />
                          <span>CHOMPED!</span>
                        </>
                      ) : (
                        <>
                          <Plus className="w-3.5 h-3.5 stroke-[3]" />
                          <span>ADD TO BAG</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>

              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
};
