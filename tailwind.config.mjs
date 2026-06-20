/** @type {import('tailwindcss').Config} */
import typography from '@tailwindcss/typography';

export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'brand-slate': '#111827',
        'brand-sand': '#faf7f2',
        'brand-blue': '#1e3a8a',
        'brand-gray': '#4b5563',
      },
      fontFamily: {
        sans: ['Lato', 'sans-serif'],
        serif: ['Playfair Display', 'serif'],
      },
      typography: ({ theme }) => ({
        DEFAULT: {
          css: {
            '--tw-prose-body': theme('colors.brand-slate'),
            '--tw-prose-headings': theme('colors.brand-slate'),
            '--tw-prose-links': theme('colors.brand-blue'),
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
}