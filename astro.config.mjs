// astro.config.mjs
import { defineConfig } from 'astro/config';

// Import all integrations at the top
import preact from '@astrojs/preact';
import tailwindcss from '@tailwindcss/vite';
import typography from '@tailwindcss/typography';

export default defineConfig({
  integrations: [
    preact()
  ],
  vite: {
    plugins: [
      tailwindcss({
        // Provide the config directly to the Vite plugin
        config: {
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
              }
            },
          },
          plugins: [typography()],
        },
      }),
    ],
  },
});