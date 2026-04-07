import type { APIRoute } from 'astro';
import { getAllWebinars } from '../data/webinars';
import { getAllTSPWebinars } from '../data/tsp-webinars';

export const prerender = false;

export const GET: APIRoute = async () => {
  const webinars = getAllWebinars();
  const tspWebinars = getAllTSPWebinars();
  const domain = 'https://planwellfp.com';

  const urls = [
    ...webinars.map(w => ({
      loc: `${domain}/webinar/${w.id}`,
      lastmod: w.date.toISOString().split('T')[0],
      priority: '0.8',
      changefreq: 'weekly'
    })),
    ...tspWebinars.map(w => ({
      loc: `${domain}/webinar/tsp/${w.id}`,
      lastmod: w.date.toISOString().split('T')[0],
      priority: '0.7',
      changefreq: 'weekly'
    }))
  ];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url>
    <loc>${u.loc}</loc>
    <lastmod>${u.lastmod}</lastmod>
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600',
    },
  });
};
