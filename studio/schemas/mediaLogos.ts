import {defineField, defineType} from 'sanity'

export default defineType({
  name: 'mediaLogos',
  title: 'Media Logos',
  type: 'document',
  fields: [
    defineField({
      name: 'items',
      title: 'Media Logos',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            defineField({
              name: 'name',
              title: 'Publication Name',
              type: 'string',
              validation: (Rule) => Rule.required(),
            }),
            defineField({
              name: 'logo',
              title: 'Logo Image',
              type: 'image',
            }),
            defineField({
              name: 'url',
              title: 'Link URL',
              type: 'url',
            }),
          ],
        },
      ],
    }),
  ],
})
