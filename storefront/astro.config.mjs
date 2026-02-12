import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://sesicthub.co.ke',
  output: 'static',
  integrations: [tailwind(), sitemap()],
  trailingSlash: 'always'
});
