'use client';

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Card, CardContent } from '@/components/ui/card';
import { useCommits } from '@/hooks/use-commits';
import useProject from '@/hooks/use-project';
import { AnimatePresence, motion } from 'framer-motion';
import { ChevronDown, GitCommit, Code } from 'lucide-react';
import { useState } from 'react';
import { LoadingSkeleton } from '../loading';
import { Badge } from '../ui/badge';

export default function CommitsFeedNeumorphic() {
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
  } = useCommits(project?.id);

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
    <div className="min-h-screen bg-gray-100 dark:bg-gray-800 p-8">
      <h1 className="text-5xl font-bold text-center mb-12 text-gray-700 dark:text-gray-200">
        Commit Chronicle
      </h1>
      <div className="max-w-4xl mx-auto space-y-8">
        {commits?.map((commit, index) => (
          <motion.div
            key={commit.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card className="overflow-hidden bg-gray-100 dark:bg-gray-800 border-none shadow-[5px_5px_15px_rgba(0,0,0,0.1),-5px_-5px_15px_rgba(255,255,255,0.1)] hover:shadow-[8px_8px_20px_rgba(0,0,0,0.1),-8px_-8px_20px_rgba(255,255,255,0.1)] transition-all duration-300">
              <CardContent className="p-0">
                <motion.div
                  layout
                  onClick={() => toggleCommit(commit.id!)}
                  className="cursor-pointer"
                >
                  <div className="relative p-6">
                    <div className="flex items-center space-x-4">
                      <Avatar className="h-16 w-16 shadow-[2px_2px_5px_rgba(0,0,0,0.1),-2px_-2px_5px_rgba(255,255,255,0.5)]">
                        <AvatarImage
                          src={commit.commit_avatar_url}
                          alt={commit.commit_author}
                        />
                        <AvatarFallback className="bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 text-xl">
                          {commit.commit_author[0].toUpperCase()}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <h2 className="text-xl font-semibold text-gray-700 dark:text-gray-200">
                          {commit.commit_message}
                        </h2>
                        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                          {commit.commit_author} •{' '}
                          {new Date(commit.commit_date).toLocaleString()}
                        </p>
                      </div>
                      <Badge
                        variant="secondary"
                        className="text-xs font-mono bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 px-3 py-1 rounded-full shadow-[2px_2px_5px_rgba(0,0,0,0.1),-2px_-2px_5px_rgba(255,255,255,0.5)]"
                      >
                        {commit.commit_hash.slice(0, 7)}
                      </Badge>
                      <motion.div
                        animate={{
                          rotate: expandedCommits.has(commit.id!) ? 180 : 0,
                        }}
                        transition={{ duration: 0.3 }}
                        className="bg-gray-200 dark:bg-gray-700 rounded-full p-2 shadow-[2px_2px_5px_rgba(0,0,0,0.1),-2px_-2px_5px_rgba(255,255,255,0.5)]"
                      >
                        <ChevronDown className="w-6 h-6 text-gray-500 dark:text-gray-400" />
                      </motion.div>
                    </div>
                  </div>
                </motion.div>
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
                      <div className="bg-gray-200 dark:bg-gray-700 p-6 shadow-[inset_5px_5px_10px_rgba(0,0,0,0.1),inset_-5px_-5px_10px_rgba(255,255,255,0.1)]">
                        <motion.h4
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.2 }}
                          className="text-gray-700 dark:text-gray-200 font-semibold mb-4 flex items-center text-lg"
                        >
                          <GitCommit className="mr-2 h-5 w-5" />
                          Commit Details
                        </motion.h4>
                        <ul className="space-y-3">
                          {(commit.commit_summary as unknown as string[]).map(
                            (summaryPoint, index) => (
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
                                <Code className="w-5 h-5 text-gray-500 dark:text-gray-400 mr-3 flex-shrink-0 mt-1" />
                                <span className="text-gray-600 dark:text-gray-300">
                                  {summaryPoint}
                                </span>
                              </motion.li>
                            ),
                          )}
                        </ul>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
