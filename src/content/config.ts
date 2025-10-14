// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const projectsCollection = defineCollection({
  type: 'content', // 'content' for Markdown files
  schema: z.object({
    title: z.string(),
    client: z.string(),
    year: z.number(),
    tags: z.array(z.string()),
    isFeatured: z.boolean().optional(),
  }),
});

export const collections = {
  'projects': projectsCollection,
};