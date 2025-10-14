// astro.config.mjs
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// --- ADD THIS LINE ---
import typography from '@tailwindcss/typography';

// https://astro.build/config
export default defineConfig({
  vite: {
    plugins: [
      // Pass the configuration object directly to the plugin
      tailwindcss({
        plugins: [
          typography(), // <-- Add the plugin here
        ],
      }),
    ],
  },
});