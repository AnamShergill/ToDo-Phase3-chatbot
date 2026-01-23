/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Neon Detonator Theme Colors
        'bg-app': '#070B14',
        'surface': '#0F172A',
        'highlight-primary': '#A855F7',
        'highlight-secondary': '#22D3EE',
        'success': '#4ADE80',
        'warning': '#FACC15',
        'danger': '#F43F5E',
        'text-primary': '#E5E7EB',
        'text-muted': '#94A3B8',
        'border': '#1E293B',
      },
      boxShadow: {
        'neon-purple': '0 0 10px rgba(168, 85, 247, 0.5)',
        'neon-cyan': '0 0 10px rgba(34, 211, 238, 0.5)',
        'neon-green': '0 0 10px rgba(74, 222, 128, 0.5)',
        'neon-red': '0 0 10px rgba(244, 63, 94, 0.5)',
        'neon-yellow': '0 0 10px rgba(250, 204, 21, 0.5)',
        'neon-purple-intense': '0 0 20px rgba(168, 85, 247, 0.8), 0 0 30px rgba(168, 85, 247, 0.4)',
        'neon-cyan-intense': '0 0 20px rgba(34, 211, 238, 0.8), 0 0 30px rgba(34, 211, 238, 0.4)',
      },
      animation: {
        'pulse-neon': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow-fade': 'glowFade 1.5s ease-in-out infinite alternate',
      },
      keyframes: {
        glowFade: {
          '0%, 100%': {
            boxShadow: '0 0 10px rgba(168, 85, 247, 0.5)'
          },
          '50%': {
            boxShadow: '0 0 20px rgba(168, 85, 247, 0.8), 0 0 30px rgba(168, 85, 247, 0.4)'
          },
        }
      },
      transitionDuration: {
        '200': '200ms',
        '300': '300ms',
      },
      transitionTimingFunction: {
        'neon': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
    },
  },
  plugins: [],
}