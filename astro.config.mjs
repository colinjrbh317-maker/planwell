// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
    site: 'https://planwellfp.com',
    integrations: [
        sitemap({
            changefreq: 'weekly',
            priority: 0.7,
            lastmod: new Date(),
        }),
    ],
    image: {
        service: {
            entrypoint: 'astro/assets/services/sharp',
        },
    },
    redirects: {
        '/resources': '/blog',
        '/resources/[slug]': '/blog/[slug]',
    },
});
