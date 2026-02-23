import {defineField, defineType} from 'sanity'

export default defineType({
  name: 'testimonials',
  title: 'Testimonials',
  type: 'document',
  fields: [
    defineField({
      name: 'items',
      title: 'Testimonial Items',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            defineField({
              name: 'quote',
              title: 'Quote',
              type: 'text',
              validation: (Rule) => Rule.required(),
            }),
            defineField({
              name: 'authorName',
              title: 'Author Name',
              type: 'string',
              validation: (Rule) => Rule.required(),
            }),
            defineField({
              name: 'authorTitle',
              title: 'Author Title / Role',
              type: 'string',
            }),
            defineField({
              name: 'rating',
              title: 'Rating (1-5)',
              type: 'number',
              validation: (Rule) => Rule.min(1).max(5),
            }),
          ],
        },
      ],
    }),
  ],
})
