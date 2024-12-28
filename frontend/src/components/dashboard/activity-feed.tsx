'use client';

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import useProject from '@/hooks/use-project';
import { GetCommits } from '@/queries/getCommits';
import { CommitType } from '@/types';
import { useQuery } from '@tanstack/react-query';
import { AxiosError } from 'axios';
import { AnimatePresence, motion } from 'framer-motion';
import { ChevronDown, GitCommit } from 'lucide-react';
import { useState } from 'react';
import { LoadingSkeleton } from '../loading';
import { Badge } from '../ui/badge';

export default function CommitsFeed() {
  const [expandedCommits, setExpandedCommits] = useState<Set<number>>(
    new Set(),
  );
  const { project } = useProject();
  const toggleCommit = (id: number) => {
    setExpandedCommits((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };
  const {
    data: commits,
    isLoading: isLoadingCommits,
    isError,
  } = useQuery<CommitType[], AxiosError>({
    queryKey: ['commits', project?.id],
    queryFn: () => GetCommits(project?.id),
    retry: false,
    staleTime: 5 * 60 * 1000,
    gcTime: 30 * 60 * 1000,
  });
  console.log('NEW COMMITS ARE ', commits);
  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>
          {'An error occurred while fetching commits.'}
        </AlertDescription>
      </Alert>
    );
  }
  if (isLoadingCommits) {
    return <LoadingSkeleton />;
  }
  return (
    <Card className="w-full min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900 dark:to-pink-900 rounded-none border-none shadow-none">
      <CardContent className="p-6">
        <div className="space-y-6">
          {commits?.map((commit, index) => (
            <motion.div
              key={commit.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <motion.div
                layout
                onClick={() => toggleCommit(commit.id!)}
                className="cursor-pointer"
              >
                <Card className="overflow-hidden transition-all duration-300 ease-in-out hover:shadow-lg dark:bg-gray-800 border border-purple-200 dark:border-purple-700">
                  <CardHeader className="flex flex-row items-start gap-4 p-4">
                    <Avatar className="h-10 w-10 border-2 border-purple-300 dark:border-purple-600">
                      <AvatarImage
                        src={commit.commit_avatar_url}
                        alt={commit.commit_author}
                      />
                      <AvatarFallback className="bg-purple-500 text-white">
                        {commit.commit_author[0].toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <CardTitle className="text-base font-semibold text-purple-800 dark:text-purple-200">
                        {commit.commit_message}
                      </CardTitle>
                      <CardDescription className="text-sm text-purple-600 dark:text-purple-400 mt-1">
                        {commit.commit_author} •{' '}
                        {new Date(commit.commit_date).toLocaleString()}
                      </CardDescription>
                    </div>
                    <Badge
                      variant="secondary"
                      className="text-xs font-mono bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-200"
                    >
                      {commit.commit_hash.slice(0, 7)}
                    </Badge>
                    <motion.div
                      animate={{
                        rotate: expandedCommits.has(commit.id!) ? 180 : 0,
                      }}
                      transition={{ duration: 0.3 }}
                      className="ml-2 p-1 rounded-full hover:bg-purple-100 dark:hover:bg-purple-800 transition-colors duration-200"
                    >
                      <ChevronDown className="w-5 h-5 text-purple-500 dark:text-purple-300" />
                    </motion.div>
                  </CardHeader>
                  <AnimatePresence initial={false}>
                    {expandedCommits.has(commit.id!) && (
                      <motion.div
                        initial="collapsed"
                        animate="expanded"
                        exit="collapsed"
                        variants={{
                          expanded: { opacity: 1, height: 'auto' },
                          collapsed: { opacity: 0, height: 0 },
                        }}
                        transition={{
                          duration: 0.4,
                          ease: [0.04, 0.62, 0.23, 0.98],
                        }}
                      >
                        <CardContent className="bg-purple-50 dark:bg-purple-900/30 p-4">
                          <motion.h4
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 }}
                            className="text-purple-700 dark:text-purple-300 font-semibold mb-2 flex items-center text-sm"
                          >
                            <GitCommit className="mr-2 h-4 w-4" />
                            Commit Summary
                          </motion.h4>
                          <ul className="space-y-2">
                            {commit &&
                              (
                                commit.commit_summary as unknown as string[]
                              ).map((summaryPoint, index) => (
                                <motion.li
                                  key={index}
                                  initial={{ opacity: 0, x: -20 }}
                                  animate={{ opacity: 1, x: 0 }}
                                  transition={{
                                    duration: 0.3,
                                    delay: 0.1 + index * 0.1,
                                  }}
                                  className="flex items-start text-sm"
                                >
                                  <span className="text-purple-500 dark:text-purple-400 mr-2">
                                    •
                                  </span>
                                  <span className="text-gray-700 dark:text-gray-300">
                                    {summaryPoint}
                                  </span>
                                </motion.li>
                              ))}
                          </ul>
                        </CardContent>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </Card>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
