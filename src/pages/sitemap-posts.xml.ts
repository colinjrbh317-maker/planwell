import type { APIRoute } from 'astro';
import { sanityClient } from '../lib/sanity';

export const prerender = false;

export const GET: APIRoute = async () => {
    const posts = await sanityClient.fetch(`
        *[_type == "post" && (!defined(publishedAt) || publishedAt <= now())] | order(publishedAt desc) {
            "slug": slug.current,
            publishedAt
        }
    `);

    const urls = posts.map((post: { slug: string; publishedAt: string }) => {
        const lastmod = post.publishedAt
            ? new Date(post.publishedAt).toISOString()
            : new Date().toISOString();
        return `  <url>
    <loc>https://planwellfp.com/${post.slug}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>`;
    });

    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.join('\n')}
</urlset>`;

    return new Response(xml, {
        headers: {
            'Content-Type': 'application/xml',
            'Cache-Control': 'public, max-age=3600',
        },
    });
};
