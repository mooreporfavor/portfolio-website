// astro.config.mjs
import { defineConfig, passthroughImageService } from 'astro/config';
import preact from '@astrojs/preact';
import tailwind from '@astrojs/tailwind';

import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.ryanamoore.com',
  integrations: [preact(), tailwind(), sitemap()],
  image: {
    service: passthroughImageService()
  }
});