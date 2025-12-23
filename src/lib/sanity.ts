import { createClient } from '@sanity/client';

export const sanityClient = createClient({
    projectId: 'nwzt57tx',
    dataset: 'production',
    useCdn: true,
    apiVersion: '2024-01-01',
});

// Blog post list query with author details
export async function getBlogPosts() {
    return await sanityClient.fetch(`
    *[_type == "post"] | order(publishedAt desc) {
      _id,
      title,
      "slug": slug.current,
      publishedAt,
      excerpt,
      readTime,
      author->{
        name,
        "slug": slug.current,
        credentials,
        title,
        bioShort,
        image {
          asset->{url}
        }
      },
      category->{
        title,
        "slug": slug.current
      },
      mainImage {
        asset->{url}
      }
    }
  `);
}

// Single blog post query with full author details
export async function getBlogPost(slug: string) {
    return await sanityClient.fetch(`
    *[_type == "post" && slug.current == $slug][0] {
      _id,
      title,
      "slug": slug.current,
      publishedAt,
      body,
      excerpt,
      readTime,
      author->{
        name,
        "slug": slug.current,
        credentials,
        title,
        bioShort,
        bioFull,
        email,
        phone,
        image {
          asset->{url}
        }
      },
      category->{
        title,
        "slug": slug.current
      },
      mainImage {
        asset->{url}
      }
    }
  `, { slug });
}

// Get posts by category
export async function getBlogPostsByCategory(categorySlug: string) {
    return await sanityClient.fetch(`
    *[_type == "post" && category->slug.current == $categorySlug] | order(publishedAt desc) {
      _id,
      title,
      "slug": slug.current,
      publishedAt,
      excerpt,
      readTime,
      author->{
        name,
        "slug": slug.current,
        image {
          asset->{url}
        }
      },
      category->{
        title,
        "slug": slug.current
      },
      mainImage {
        asset->{url}
      }
    }
  `, { categorySlug });
}

// Get posts by author
export async function getBlogPostsByAuthor(authorSlug: string) {
    return await sanityClient.fetch(`
    *[_type == "post" && author->slug.current == $authorSlug] | order(publishedAt desc) {
      _id,
      title,
      "slug": slug.current,
      publishedAt,
      excerpt,
      readTime,
      author->{
        name,
        "slug": slug.current,
        image {
          asset->{url}
        }
      },
      category->{
        title,
        "slug": slug.current
      },
      mainImage {
        asset->{url}
      }
    }
  `, { authorSlug });
}

// Get all categories with post count
export async function getCategories() {
    return await sanityClient.fetch(`
    *[_type == "category"] {
      _id,
      title,
      "slug": slug.current,
      description,
      "postCount": count(*[_type == "post" && references(^._id)])
    } | order(postCount desc)
  `);
}

// Get all authors
export async function getAuthors() {
    return await sanityClient.fetch(`
    *[_type == "author"] {
      _id,
      name,
      "slug": slug.current,
      credentials,
      title,
      bioShort,
      bioFull,
      email,
      phone,
      image {
        asset->{url}
      }
    }
  `);
}
