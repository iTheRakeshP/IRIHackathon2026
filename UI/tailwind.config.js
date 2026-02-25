/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  safelist: [
    'bg-gradient-to-br',
    'bg-gradient-to-r',
    'from-indigo-500',
    'from-indigo-600',
    'to-purple-600',
    'to-purple-700',
    'to-purple-800',
    'from-red-500',
    'to-red-700',
    'to-rose-600',
    'from-purple-600',
    'from-purple-800',
    'from-amber-500',
    'from-amber-400',
    'to-amber-600',
    'to-orange-500',
    'to-orange-600',
    'from-emerald-500',
    'to-teal-600',
    'from-rose-500',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        secondary: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#a855f7',
          600: '#9333ea',
          700: '#7e22ce',
          800: '#6b21a8',
          900: '#581c87',
        },
      },
      animation: {
        'fadeInUp': 'fadeInUp 0.6s ease-out',
      },
      keyframes: {
        fadeInUp: {
          '0%': {
            opacity: '0',
            transform: 'translateY(20px)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
      },
    },
  },
  plugins: [],
}
