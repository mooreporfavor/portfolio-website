/** @type {import('tailwindcss').Config} */
import typography from '@tailwindcss/typography';

export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'brand-slate': '#0f172a',
        'brand-navy': '#090d16',
        'brand-sand': '#faf8f5',
        'brand-canvas': '#f8fafc',
        'brand-blue': '#1e3a8a',
        'brand-accent': '#2563eb',
        'brand-cyan': '#0284c7',
        'brand-emerald': '#059669',
        'brand-amber': '#d97706',
        'brand-gray': '#475569',
        'brand-muted': '#64748b',
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Lato', 'Inter', 'system-ui', 'sans-serif'],
        serif: ['Playfair Display', 'Newsreader', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(15, 23, 42, 0.07)',
        'glow': '0 0 30px -5px rgba(37, 99, 235, 0.25)',
        'glow-emerald': '0 0 30px -5px rgba(5, 150, 105, 0.25)',
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 10px 25px -5px rgba(0, 0, 0, 0.03)',
        'card-hover': '0 20px 40px -12px rgba(15, 23, 42, 0.12), 0 0 1px 1px rgba(15, 23, 42, 0.05)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-subtle': 'pulseSubtle 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2.5s infinite linear',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      typography: ({ theme }) => ({
        DEFAULT: {
          css: {
            '--tw-prose-body': theme('colors.brand-slate'),
            '--tw-prose-headings': theme('colors.brand-slate'),
            '--tw-prose-links': theme('colors.brand-accent'),
          },
        },
        lg: {
          css: {
            'h1, h2, h3, h4, h5, h6': {
              fontFamily: theme('fontFamily.serif'),
            },
          },
        },
      }),
    },
  },
  plugins: [
    typography,
  ],
};