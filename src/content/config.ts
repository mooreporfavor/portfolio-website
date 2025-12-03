// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const projectsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    client: z.string(),
    year: z.number(),
    track: z.string(),
    tags: z.array(z.string()),
    isFeatured: z.boolean().optional(),
    heroImage: z.string().optional(),
  }),
});

export const collections = {
  'projects': projectsCollection,
};