import { z } from 'zod';
export const Project = z.object({
  id: z.number().optional(),
  github_url: z.string().url().startsWith('https://github.com/'),
  name: z.string().min(1, 'Project name is required'),
  description: z.string().optional(),
});
