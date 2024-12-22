"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import useProject from "@/hooks/use-project";
import { ProjectType } from "@/types";
import { useAuth } from "@clerk/nextjs";
import { useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { motion } from "framer-motion";
import { ExternalLinkIcon, GitlabIcon as GitHubIcon } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";

export function TopBar() {
  const { project, projects, setSelectedProjectId } = useProject();
  if (!projects) return null;
  const { getToken } = useAuth();
  const queryClient = useQueryClient();

  if (!project) return null;
  return (
    <motion.div
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="flex items-center justify-between mb-8"
    >
      <Link rel="noopener noreferrer" target="_blank" href={project.github_url}>
        <Button
          rel="noopener noreferrer"
          className="bg-purple-600 hover:bg-purple-700 text-white flex items-center gap-2"
        >
          <GitHubIcon className="h-4 w-4" />
          {project.github_url}
          <ExternalLinkIcon className="h-4 w-4" />
        </Button>
      </Link>
      <div className="flex items-center gap-4">
        <Button variant="ghost" className="flex items-center gap-2">
          <Avatar className="h-6 w-6">
            <AvatarImage src="/placeholder.svg?height=24&width=24" />
            <AvatarFallback>U</AvatarFallback>
          </Avatar>
          Invite a team member!
        </Button>
        <Button
          onClick={async () => {
            const token = await getToken();
            const oldProjectId: ProjectType = project;
            try {
              console.log("inside try");
              queryClient.setQueryData(["projects", "persist"], () => {
                const updateProjects = projects.filter(
                  (p) => p.id !== oldProjectId.id,
                );

                if (updateProjects[0].id === undefined) {
                  toast.warning("No projects found");
                }
                setSelectedProjectId(
                  updateProjects.length > 0 ? updateProjects[0].id! : 0,
                );
                return updateProjects;
              });
              toast.success("Project deleted successfully");

              await axios.delete(
                `${process.env.NEXT_PUBLIC_BACKEND_API}users/delete-project`,
                {
                  data: { project_id: oldProjectId.id },
                  headers: {
                    Authorization: `Bearer ${token}`,
                  },
                },
              );

              queryClient.invalidateQueries({
                queryKey: ["projects", "persist"],
              });
            } catch (error) {
              queryClient.setQueryData(["projects", "persist"], () => {
                setSelectedProjectId(oldProjectId.id!);
                return [...projects, oldProjectId];
              });
              toast.error("Error deleting project");
            }
          }}
          variant="ghost"
        >
          Delete Project
        </Button>
      </div>
    </motion.div>
  );
}
