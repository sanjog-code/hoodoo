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
          canvas: 'var(--bg-canvas)',
          surface: 'var(--bg-surface)',
          elevated: 'var(--bg-surface-elevated)',
          darkBg: '#0a0a0c',
          darkCard: '#121215',
          lightBg: '#f5f5f4',
          lightCard: '#ffffff',
          accent: '#18181b',
        }
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        display: ['"Clash Display"', '"Syne"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        street: ['"Syne"', '"Clash Display"', 'sans-serif'],
        gothic: ['"Cinzel"', 'serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        'brutal': '3px 3px 0px 0px rgba(0,0,0,1)',
        'soft-glow': '0 20px 50px -10px rgba(0, 0, 0, 0.08)',
        'dark-glow': '0 20px 50px -10px rgba(0, 0, 0, 0.6)',
      },
    },
  },
  plugins: [],
}
