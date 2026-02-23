import {defineConfig} from 'sanity'
import {structureTool} from 'sanity/structure'
import {visionTool} from '@sanity/vision'
import {schemaTypes} from './schemas'

export default defineConfig({
  name: 'planwell',
  title: 'PlanWell Financial Planning',
  projectId: 'nwzt57tx',
  dataset: 'production',
  plugins: [
    structureTool({
      structure: (S) =>
        S.list()
          .title('Content')
          .items([
            S.listItem()
              .title('Blog Posts')
              .schemaType('post')
              .child(S.documentTypeList('post').title('Blog Posts')),
            S.listItem()
              .title('Authors')
              .schemaType('author')
              .child(S.documentTypeList('author').title('Authors')),
            S.listItem()
              .title('Categories')
              .schemaType('category')
              .child(S.documentTypeList('category').title('Categories')),
            S.divider(),
            S.listItem()
              .title('Homepage')
              .child(
                S.list()
                  .title('Homepage Sections')
                  .items([
                    S.listItem()
                      .title('Hero Section')
                      .child(
                        S.document()
                          .schemaType('homepageHero')
                          .documentId('homepageHero')
                      ),
                    S.listItem()
                      .title('Testimonials')
                      .child(
                        S.document()
                          .schemaType('testimonials')
                          .documentId('testimonials')
                      ),
                    S.listItem()
                      .title('FAQ Section')
                      .child(
                        S.document()
                          .schemaType('faqSection')
                          .documentId('faqSection')
                      ),
                    S.listItem()
                      .title('Media Logos')
                      .child(
                        S.document()
                          .schemaType('mediaLogos')
                          .documentId('mediaLogos')
                      ),
                  ])
              ),
          ]),
    }),
    visionTool(),
  ],
  schema: {
    types: schemaTypes,
  },
})
