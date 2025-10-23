// astro.config.mjs
import { defineConfig, passthroughImageService } from 'astro/config';
import preact from '@astrojs/preact';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [preact(), tailwind()],
  image: {
    service: passthroughImageService()
  }
});