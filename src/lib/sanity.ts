import { createClient } from '@sanity/client';

export const sanityClient = createClient({
    projectId: 'nwzt57tx',
    dataset: 'production',
    useCdn: true,
    apiVersion: '2024-01-01',
});

export async function getBlogPosts() {
    return await sanityClient.fetch(`
    *[_type == "post"] | order(publishedAt desc) {
      _id,
      title,
      slug,
      publishedAt,
      excerpt,
      "author": author->name,
      "category": category->title,
      mainImage {
        asset->{url}
      }
    }
  `);
}

export async function getBlogPost(slug: string) {
    return await sanityClient.fetch(`
    *[_type == "post" && slug.current == $slug][0] {
      _id,
      title,
      slug,
      publishedAt,
      body,
      excerpt,
      "author": author->name,
      "category": category->title,
      mainImage {
        asset->{url}
      }
    }
  `, { slug });
}
