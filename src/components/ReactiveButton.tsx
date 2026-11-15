import React, { useRef, useState } from 'react';

// Shared Web Audio API Synthesizer for Gen Z Haptics
class SoundFXEngine {
  private ctx: AudioContext | null = null;
  public enabled: boolean = true;

  private init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      this.ctx = new AudioCtx();
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  // Realistic Procedural Crunch / Bite Sound
  playCrunch() {
    if (!this.enabled) return;
    try {
      this.init();
      if (!this.ctx) return;
      const ctx = this.ctx;

      // 1. Noise Burst (Crispy bun & cucumber crunch)
      const bufferSize = ctx.sampleRate * 0.08;
      const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.25));
      }

      const noise = ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(1400, ctx.currentTime);
      filter.Q.setValueAtTime(3.0, ctx.currentTime);

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.35, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      noise.start();

      // 2. Sub impact thud (Heavy beef smash bite)
      const osc = ctx.createOscillator();
      const oscGain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(160, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(40, ctx.currentTime + 0.07);

      oscGain.gain.setValueAtTime(0.4, ctx.currentTime);
      oscGain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.07);

      osc.connect(oscGain);
      oscGain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.07);
    } catch {
      // Audio blocked or not permitted
    }
  }

  playPop(freq = 880) {
    if (!this.enabled) return;
    try {
      this.init();
      if (!this.ctx) return;
      const ctx = this.ctx;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, ctx.currentTime);
      gain.gain.setValueAtTime(0.06, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.03);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.03);
    } catch {}
  }
}

export const sfx = new SoundFXEngine();

interface ReactiveButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost' | 'neon';
  sound?: 'crunch' | 'pop' | 'none';
  children: React.ReactNode;
  className?: string;
}

export const ReactiveButton: React.FC<ReactiveButtonProps> = ({
  variant = 'primary',
  sound = 'crunch',
  children,
  className = '',
  onClick,
  ...props
}) => {
  const [particles, setParticles] = useState<{ id: number; x: number; y: number; color: string }[]>([]);
  const btnRef = useRef<HTMLButtonElement>(null);

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    // Sound synthesis
    if (sound === 'crunch') {
      sfx.playCrunch();
    } else if (sound === 'pop') {
      sfx.playPop();
    }

    // Trigger visual confetti particles
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    const colors = ['#f59e0b', '#a3e635', '#ef4444', '#fde047', '#ffffff'];
    const newParticles = Array.from({ length: 8 }).map((_, i) => ({
      id: Date.now() + i,
      x: clickX,
      y: clickY,
      color: colors[Math.floor(Math.random() * colors.length)],
    }));

    setParticles(newParticles);
    setTimeout(() => setParticles([]), 700);

    if (onClick) onClick(e);
  };

  const variantStyles = {
    primary:
      'bg-gradient-to-r from-amber-500 via-amber-400 to-yellow-400 text-neutral-950 font-black shadow-[0_6px_0_#92400e,0_12px_24px_rgba(245,158,11,0.4)] hover:brightness-105 active:shadow-[0_2px_0_#92400e] active:translate-y-[4px]',
    secondary:
      'bg-neutral-900 text-white border border-neutral-700 shadow-[0_6px_0_#262626] hover:border-amber-400 active:shadow-[0_2px_0_#262626] active:translate-y-[4px]',
    danger:
      'bg-gradient-to-r from-red-600 to-orange-600 text-white font-black shadow-[0_6px_0_#991b1b,0_12px_24px_rgba(239,68,68,0.4)] active:shadow-[0_2px_0_#991b1b] active:translate-y-[4px]',
    neon:
      'bg-lime-400 text-neutral-950 font-black shadow-[0_6px_0_#4d7c0f,0_12px_24px_rgba(163,230,53,0.5)] active:shadow-[0_2px_0_#4d7c0f] active:translate-y-[4px]',
    ghost:
      'bg-transparent text-neutral-300 hover:text-white hover:bg-neutral-800/60 active:translate-y-[1px]',
  }[variant];

  return (
    <button
      ref={btnRef}
      onClick={handleClick}
      className={`relative overflow-hidden rounded-xl px-6 py-3 font-sans text-sm tracking-wide uppercase transition-all duration-100 flex items-center justify-center gap-2 select-none group ${variantStyles} ${className}`}
      {...props}
    >
      {/* Glint line */}
      <span className="absolute top-0 left-0 right-0 h-[2px] bg-white/40 opacity-70 pointer-events-none" />

      {/* Children Content */}
      <span className="relative z-10 flex items-center gap-2">
        {children}
      </span>

      {/* Particle Bursts */}
      {particles.map((p, idx) => {
        const angle = (idx / particles.length) * Math.PI * 2;
        const dist = 32 + Math.random() * 24;
        const dx = Math.cos(angle) * dist;
        const dy = Math.sin(angle) * dist;
        return (
          <span
            key={p.id}
            className="absolute w-2 h-2 rounded-full pointer-events-none animate-ping"
            style={{
              left: `${p.x}px`,
              top: `${p.y}px`,
              backgroundColor: p.color,
              transform: `translate(${dx}px, ${dy}px)`,
              transition: 'all 500ms ease-out',
            }}
          />
        );
      })}
    </button>
  );
};
