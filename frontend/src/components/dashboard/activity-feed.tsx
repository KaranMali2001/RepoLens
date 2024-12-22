"use client";

import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useQuery } from "@tanstack/react-query";
import { GetCommits } from "@/queries/getCommits";
import useProject from "@/hooks/use-project";
import { CommitType } from "@/types";
import { AxiosError } from "axios";

export default function CommitsFeed() {
  const { project } = useProject();
  if (!project || !project.id) return null;
  const {
    data: commits,
    isLoading,
    isError,
  } = useQuery<CommitType[], AxiosError>({
    queryKey: ["commits"],
    queryFn: () => GetCommits(project?.id!),
    retry: false,
  });
  console.log("data ", commits);
  if (isError) {
    return <div>Error fetching commits</div>;
  }
  if (isLoading) {
    return <div>Loading...</div>;
  }
  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ delay: 0.3 }}
      className="space-y-6"
    >
      {commits?.map((commit) => (
        <Card key={commit.id} className="overflow-hidden">
          <CardContent className="p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <Avatar>
                  <AvatarImage src={commit.commit_avatar_url} />
                  <AvatarFallback>{commit.commit_author[0]}</AvatarFallback>
                </Avatar>
                <div>
                  <span className="font-medium">{commit.commit_author}</span>{" "}
                  <span className="text-gray-500">{commit.commit_message}</span>
                </div>
              </div>
              <span className="text-sm text-gray-500">
                {commit.commit_date}
              </span>
            </div>
            {/* <h3 className="text-lg font-semibold mb-4">
              {commit.commit_summary}
            </h3> */}
            <div className="bg-gray-50 p-4 rounded-lg font-mono text-sm">
              {commit.commit_summary}
            </div>
          </CardContent>
        </Card>
      ))}
    </motion.div>
  );
}
