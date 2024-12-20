"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { GitlabIcon as GitHubIcon } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { createProjects } from "@/queries/createProjects";
import { Project } from "@/schemas/ProjectInput";
import { ProjectType } from "@/types";

export default function CreateProjectPage() {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState<ProjectType>({
    github_url: "",
    name: "",
    description: "",
  });

  const createProject = useMutation({
    mutationFn: (reqData: ProjectType) => createProjects(reqData),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["projects"],
      });
      toast.success("Project Created Successfully");
      setFormData({
        github_url: "",
        name: "",
        description: "",
      });
    },
    onError: () => {
      toast.error("Error creating project");
    },
  });

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const validation = Project.safeParse(formData);
    if (!validation.success) {
      toast.error(validation.error.errors[0].message);
      return;
    }
    createProject.mutate(formData);
  };

  return (
    <div className="h-full flex items-center justify-center">
      <div className="w-full max-w-2xl flex flex-col items-center justify-center gap-8">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="text-gray-300"
        >
          <GitHubIcon className="w-20 h-20" />
        </motion.div>

        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="w-full"
        >
          <Card className="border-0 shadow-sm">
            <CardHeader>
              <CardTitle className="text-xl font-semibold">
                Link your Github repo
              </CardTitle>
            </CardHeader>
            <form onSubmit={handleSubmit}>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label className="text-sm text-gray-600">
                    Github Repository URL
                  </Label>
                  <Input
                    name="github_url"
                    value={formData.github_url}
                    onChange={handleInputChange}
                    placeholder="https://github.com/username/repo"
                    className="h-10 border-gray-200"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-sm text-gray-600">Project Name</Label>
                  <Input
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="My Awesome Project"
                    className="h-10 border-gray-200"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label className="text-sm text-gray-600">
                    Project Description
                  </Label>
                  <Textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    placeholder="Briefly describe your project"
                    className="min-h-[100px] border-gray-200 resize-none"
                  />
                </div>
                <Button
                  type="submit"
                  className="w-full bg-[#7C3AED] hover:bg-[#6D28D9] text-white h-10 mt-2"
                  disabled={createProject.isPending}
                >
                  {createProject.isPending
                    ? "Creating Project..."
                    : "Create Project"}
                </Button>
              </CardContent>
            </form>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
