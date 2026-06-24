
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        
        base:     '#0A0A0F',
        surface:  '#13131A',
        elevated: '#1E1E2E',
        border:   '#2A2A3E',

    
        'text-primary':   '#E2E8F0',
        'text-secondary': '#94A3B8',
        'text-muted':     '#4A5568',

        indigo:  '#6366F1',
        'indigo-dim': '#4338CA',
        cyan:    '#22D3EE',
        'cyan-dim': '#0891B2',
      },
      fontFamily: {
        
        sans: ['Inter', 'system-ui', 'sans-serif'],
        
        serif: ['Newsreader', 'Georgia', 'serif'],
      },
      animation: {
        'ticker': 'ticker 40s linear infinite',
        'fade-up': 'fadeUp 0.4s ease forwards',
        'pulse-slow': 'pulse 3s ease-in-out infinite',
      },
      keyframes: {
        ticker: {
          '0%':   { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
        fadeUp: {
          '0%':   { opacity: 0, transform: 'translateY(12px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}