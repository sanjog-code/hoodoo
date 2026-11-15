/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        hoodoo: {
          green: '#22c55e',
          purple: '#581c87',
          plum: '#4c1d95',
          brandPurple: '#4c1775',
          darkBg: '#0c0a09',
          darkCard: '#171412',
          lightBg: '#ffffff',
          lightCard: '#f7f6f4',
          accent: '#18181b',
        }
      },
      fontFamily: {
        sans: ['Space Grotesk', 'Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        display: ['Syne', 'Impact', 'Bebas Neue', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
        serif: ['Playfair Display', 'Georgia', 'serif'],
      },
      boxShadow: {
        'brutal': '4px 4px 0px 0px rgba(0,0,0,1)',
        'brutal-purple': '4px 4px 0px 0px #4c1d95',
        'soft-glow': '0 20px 50px -10px rgba(0, 0, 0, 0.08)',
        'dark-glow': '0 20px 50px -10px rgba(0, 0, 0, 0.6)',
      },
      animation: {
        'float': 'float 4s ease-in-out infinite',
        'pulse-subtle': 'pulseSubtle 2.5s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-6px)' },
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.85' },
        }
      }
    },
  },
  plugins: [],
}
