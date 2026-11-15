import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, Sparkles, Flame, Tv } from 'lucide-react';
import { sfx } from './ReactiveButton';

interface VideoFeed {
  id: string;
  title: string;
  badge: string;
  channel: string;
  posterUrl: string;
  desc: string;
}

const FEEDS: VideoFeed[] = [
  {
    id: 'cyber-sizzle',
    title: '475°F NIGHT CITY MAILLARD SEAR',
    badge: 'LIVE GRIDDLE FEED',
    channel: 'GRILL-CAM #01',
    posterUrl: 'https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=1200&q=80',
    desc: '40-day dry-aged 44 Farms chuck & brisket pressed with 25kg steel irons for lacy crispy skirt edges.',
  },
  {
    id: 'molten-cheddar',
    title: 'THE DOUBLE CHEDDAR CASCADE',
    badge: 'CHEESE PULL 120FPS',
    channel: 'MACRO LENS #04',
    posterUrl: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1200&q=80',
    desc: 'Aged Wisconsin cheddar melting over two sizzling patties with caramelized Vidalia onions.',
  },
  {
    id: 'street-tokyo',
    title: 'SPIDER-VERSE BODEGA SPECIAL',
    badge: 'CHOPPED CHEESE CUT',
    channel: 'BKLYN STREET #09',
    posterUrl: 'https://images.unsplash.com/photo-1586190848861-99aa4a171e90?auto=format&fit=crop&w=1200&q=80',
    desc: 'Buttered Martin’s potato bun toasted on tallow, stacked with crunchy cucumbers and hot ghost pepper jam.',
  },
];

export const VideoWall: React.FC = () => {
  const [activeFeed, setActiveFeed] = useState<string>(FEEDS[0].id);
  const [isPlaying, setIsPlaying] = useState<boolean>(true);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Live Procedural Canvas Sizzle Simulator (Zero Network 404s/403s, 100% Offline Autonomy)
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId: number;
    let frame = 0;

    // Sizzle ember particles
    const particles = Array.from({ length: 45 }).map(() => ({
      x: Math.random() * canvas.width,
      y: canvas.height * (0.6 + Math.random() * 0.4),
      vy: 1.2 + Math.random() * 2.5,
      vx: (Math.random() - 0.5) * 1.5,
      radius: 1.5 + Math.random() * 2.5,
      alpha: 0.2 + Math.random() * 0.7,
      color: Math.random() > 0.4 ? '#f59e0b' : '#ef4444',
    }));

    const render = () => {
      if (!isPlaying) {
        animId = requestAnimationFrame(render);
        return;
      }
      frame++;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Heat wave distortion gradient
      const grad = ctx.createLinearGradient(0, canvas.height, 0, 0);
      grad.addColorStop(0, 'rgba(239, 68, 68, 0.25)');
      grad.addColorStop(0.3, 'rgba(245, 158, 11, 0.15)');
      grad.addColorStop(1, 'transparent');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw embers
      particles.forEach((p) => {
        p.y -= p.vy;
        p.x += p.vx + Math.sin(frame * 0.05 + p.y * 0.01) * 0.5;
        p.alpha -= 0.008;

        if (p.y < canvas.height * 0.2 || p.alpha <= 0) {
          p.y = canvas.height * 0.95;
          p.x = Math.random() * canvas.width;
          p.alpha = 0.4 + Math.random() * 0.6;
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.shadowBlur = 8;
        ctx.shadowColor = p.color;
        ctx.fill();
        ctx.globalAlpha = 1.0;
        ctx.shadowBlur = 0;
      });

      animId = requestAnimationFrame(render);
    };

    render();

    return () => cancelAnimationFrame(animId);
  }, [isPlaying, activeFeed]);

  const currentFeedObj = FEEDS.find(f => f.id === activeFeed) || FEEDS[0];

  return (
    <section className="w-full py-16 px-4 sm:px-8 border-y border-neutral-800/80 bg-neutral-950 relative overflow-hidden">
      
      {/* Background Neon Grid Ambience */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1f293710_1px,transparent_1px),linear-gradient(to_bottom,#1f293710_1px,transparent_1px)] bg-[size:4rem_4rem] pointer-events-none" />
      <div className="absolute -top-32 right-1/4 w-96 h-96 bg-amber-500/10 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute -bottom-32 left-1/4 w-96 h-96 bg-lime-400/10 rounded-full blur-[100px] pointer-events-none" />

      <div className="max-w-7xl mx-auto relative z-10">
        
        {/* Section Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-10 gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-500/10 border border-red-500/30 text-red-400 font-mono text-xs font-bold uppercase tracking-wider mb-2">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
              <span>LIVE KITCHEN BROADCAST // CCTV STREAM</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-white font-sans">
              WATCH THE <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-orange-400 to-red-500">KRUNCH</span> GO DOWN
            </h2>
            <p className="text-neutral-400 text-sm sm:text-base mt-1 max-w-xl">
              Zero stock footage. Live high-speed 120 FPS camera telemetry from our flat-top cast iron stations in Austin.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-mono text-neutral-400 uppercase tracking-widest hidden md:inline">
              SIGNAL: 4K HIGH BITRATE
            </span>
          </div>
        </div>

        {/* Video Reel Bento Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
          
          {/* Main Featured Video Stream (8 cols) */}
          <div className="lg:col-span-8 rounded-2xl bg-neutral-900 border-2 border-neutral-800 hover:border-amber-400/50 transition-all overflow-hidden relative group shadow-2xl flex flex-col justify-between min-h-[420px]">
            {/* VHS Scanline Overlay */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%)] bg-[length:100%_4px] z-20 pointer-events-none opacity-40" />

            {/* Video / Sizzle Stream Display */}
            <div className="relative w-full h-[320px] sm:h-[380px] bg-black overflow-hidden flex items-center justify-center">
              {/* High-res backdrop poster */}
              <img
                src={currentFeedObj.posterUrl}
                alt={currentFeedObj.title}
                className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              />

              {/* Procedural Live 60FPS Sizzle Ember Canvas */}
              <canvas
                ref={canvasRef}
                width={800}
                height={450}
                className="absolute inset-0 w-full h-full z-15 pointer-events-none"
              />

              {/* Dark Gradient Overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-neutral-950 via-transparent to-black/40 z-18 pointer-events-none" />

              {/* Live Status Overlay in Video */}
              <div className="absolute top-4 left-4 z-30 flex items-center gap-2">
                <span className="px-2.5 py-1 rounded bg-red-600/90 text-white font-mono text-[10px] font-bold tracking-widest flex items-center gap-1.5 shadow-lg">
                  <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse" />
                  REC ● 4K 120FPS
                </span>
                <span className="px-2.5 py-1 rounded bg-neutral-950/80 backdrop-blur-md text-amber-300 font-mono text-[10px] font-semibold border border-amber-500/30">
                  {currentFeedObj.channel}
                </span>
              </div>

              {/* Sound Effect & Play/Pause Trigger */}
              <div className="absolute bottom-4 right-4 z-30 flex items-center gap-2">
                <button
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-neutral-950/80 backdrop-blur-md text-white text-xs font-mono border border-neutral-700 hover:border-amber-400 transition-colors shadow-lg active:scale-95"
                >
                  {isPlaying ? <Pause className="w-3.5 h-3.5 text-amber-400" /> : <Play className="w-3.5 h-3.5 text-emerald-400" />}
                  <span>{isPlaying ? 'PAUSE FEED' : 'RESUME FEED'}</span>
                </button>

                <button
                  onClick={() => sfx.playCrunch()}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-neutral-950/80 backdrop-blur-md text-white text-xs font-mono border border-neutral-700 hover:border-amber-400 transition-colors shadow-lg active:scale-95"
                >
                  <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                  <span>SIZZLE SFX</span>
                </button>
              </div>
            </div>

            {/* Video Bottom Telemetry Card */}
            <div className="p-5 bg-gradient-to-t from-neutral-950 via-neutral-900 to-neutral-900/90 border-t border-neutral-800 z-30">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <h3 className="font-sans font-black text-lg sm:text-xl text-white tracking-tight">
                    {currentFeedObj.title}
                  </h3>
                  <p className="text-neutral-400 text-xs mt-1">
                    {currentFeedObj.desc}
                  </p>
                </div>
                <span className="px-3 py-1 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 font-mono text-xs font-bold uppercase self-start sm:self-auto">
                  {currentFeedObj.badge}
                </span>
              </div>
            </div>
          </div>

          {/* Secondary Stream Selector Rail (4 cols) */}
          <div className="lg:col-span-4 flex flex-col gap-4">
            <div className="text-xs font-mono uppercase tracking-widest text-neutral-400 flex items-center gap-2">
              <Tv className="w-4 h-4 text-amber-400" />
              <span>CHANNELS ON FLAT-TOP</span>
            </div>

            {FEEDS.map((feed) => (
              <button
                key={feed.id}
                onClick={() => {
                  setActiveFeed(feed.id);
                  sfx.playPop(1040);
                }}
                className={`p-4 rounded-xl text-left border transition-all duration-200 flex items-center gap-4 relative overflow-hidden group ${
                  activeFeed === feed.id
                    ? 'bg-neutral-900 border-amber-500 shadow-[0_0_24px_rgba(245,158,11,0.2)]'
                    : 'bg-neutral-950/70 border-neutral-800 hover:border-neutral-700 hover:bg-neutral-900/40'
                }`}
              >
                {/* Thumbnail Preview */}
                <div className="w-20 h-16 rounded-lg overflow-hidden flex-shrink-0 relative border border-neutral-800">
                  <img
                    src={feed.posterUrl}
                    alt={feed.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                  <div className="absolute inset-0 bg-neutral-950/30 flex items-center justify-center">
                    <Play className="w-4 h-4 text-white fill-current opacity-80" />
                  </div>
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono font-bold text-amber-400 uppercase">
                      {feed.channel}
                    </span>
                    {activeFeed === feed.id && (
                      <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-ping" />
                    )}
                  </div>
                  <h4 className="font-bold text-xs sm:text-sm text-white truncate mt-0.5">
                    {feed.title}
                  </h4>
                  <p className="text-[11px] text-neutral-400 truncate mt-0.5">
                    {feed.badge}
                  </p>
                </div>
              </button>
            ))}

            {/* Telemetry Micro Box */}
            <div className="mt-auto p-4 rounded-xl bg-neutral-900/60 border border-neutral-800/80 font-mono text-xs text-neutral-400 flex flex-col gap-1.5">
              <div className="flex justify-between">
                <span>BITRATE:</span>
                <span className="text-white font-bold tabular-nums">48.2 MBPS</span>
              </div>
              <div className="flex justify-between">
                <span>GRIDDLE TEMP:</span>
                <span className="text-amber-400 font-bold tabular-nums">475.6°F</span>
              </div>
              <div className="flex justify-between">
                <span>FPS SYNC:</span>
                <span className="text-lime-400 font-bold tabular-nums">120.0 FPS</span>
              </div>
            </div>

          </div>

        </div>

      </div>
    </section>
  );
};
