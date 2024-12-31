'use client';

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import useProject from '@/hooks/use-project';
import { ProjectType } from '@/types';
import { useAuth } from '@clerk/nextjs';
import { useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { motion } from 'framer-motion';
import {
  Delete,
  DeleteIcon,
  ExternalLinkIcon,
  GitlabIcon as GitHubIcon,
  LucideTrash2,
} from 'lucide-react';
import Link from 'next/link';
import { toast } from 'sonner';

export function TopBar() {
  const queryClient = useQueryClient();
  const { getToken } = useAuth();
  const { project, projects, setSelectedProjectId } = useProject();
  if (!projects) return null;

  if (!project) return null;
  return (
    <motion.div
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="flex items-center justify-between mb-8 "
    >
      <Link rel="noopener noreferrer" target="_blank" href={project.github_url}>
        <Button
          effect="shineHover"
          rel="noopener noreferrer"
          className=" flex items-center gap-2 bg-primary text-foreground"
        >
          <GitHubIcon className="h-4 w-4" />
          {project.github_url}
          <ExternalLinkIcon className="h-4 w-4" />
        </Button>
      </Link>
      <div className="flex items-center gap-4 ">
        <div className="bg-black text-white">
          <Button variant="ghost" className="flex items-center gap-2">
            Invite a team member!
          </Button>
        </div>
        <Button
          onClick={async () => {
            const token = await getToken();
            const oldProjectId: ProjectType = project;
            try {
              console.log('inside try');

              await axios.delete(
                `${process.env.NEXT_PUBLIC_BACKEND_API}users/delete-project`,
                {
                  data: { project_id: oldProjectId.id },
                  headers: {
                    Authorization: `Bearer ${token}`,
                  },
                },
              );
              toast.success('Project deleted successfully');
            } catch (error: unknown) {
              console.log('error', error);
              toast.error('Error deleting project');
            } finally {
              queryClient.invalidateQueries({
                queryKey: ['projects', 'persist'],
              });
              setSelectedProjectId(projects[0].id!);
            }
          }}
          variant="destructive"
          effect="expandIcon"
          icon={LucideTrash2}
          iconPlacement="right"
        >
          Delete Project
        </Button>
      </div>
    </motion.div>
  );
}
