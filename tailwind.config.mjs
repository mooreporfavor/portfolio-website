/** @type {import('tailwindcss').Config} */
import typography from '@tailwindcss/typography';

export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'brand-slate': '#1a202c',
        'brand-sand': '#f7fafc',
        'brand-blue': '#2b6cb0',
        'brand-gray': '#a0aec0',
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