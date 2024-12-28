import { z } from 'zod';

export const Commit = z.object({
  id: z.number().optional(),
  commit_hash: z.string().min(1, 'Commit hash is required'),
  commit_author: z.string().min(1, 'Commit author is required'),
  commit_message: z.string().min(1, 'Commit message is required'),
  commit_date: z.string().min(1, 'Commit date is required'),
  commit_summary: z.string().min(1, 'Commit summary is required').optional(),
  commit_avatar_url: z.string().url().optional(),
});
