'use client';

import { motion } from 'framer-motion';
import { Code, GitCommit } from 'lucide-react';

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { CommitExpandButton } from '@/components/dashboard/Commits/commit-expand';
import type { CommitType } from '@/types';

interface CommitCardProps {
  commit: CommitType;
  isExpanded: boolean;
  onToggle: () => void;
  index: number;
}

export function CommitCard({
  commit,
  isExpanded,
  onToggle,
  index,
}: CommitCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
    >
      <Card className="overflow-hidden border-none bg-white/5 shadow-[5px_5px_15px_rgba(0,0,0,0.1),-5px_-5px_15px_rgba(255,255,255,0.05)] hover:shadow-[8px_8px_20px_rgba(0,0,0,0.1),-8px_-8px_20px_rgba(255,255,255,0.05)] transition-all duration-300 dark:bg-gray-800/50">
        <CardContent className="p-0">
          <motion.div layout onClick={onToggle} className="cursor-pointer">
            <div className="relative p-6">
              <div className="flex items-center space-x-4">
                <Avatar className="h-16 w-16 ring-2 ring-primary/20 shadow-[2px_2px_5px_rgba(0,0,0,0.1),-2px_-2px_5px_rgba(255,255,255,0.1)]">
                  <AvatarImage
                    src={commit.commit_avatar_url}
                    alt={commit.commit_author}
                  />
                  <AvatarFallback className="bg-primary/10 text-primary text-xl">
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
                  className="text-xs font-mono bg-primary/10 text-primary px-3 py-1 rounded-full shadow-[2px_2px_5px_rgba(0,0,0,0.1),-2px_-2px_5px_rgba(255,255,255,0.1)]"
                >
                  {commit.commit_hash.slice(0, 7)}
                </Badge>
                <CommitExpandButton isExpanded={isExpanded} />
              </div>
            </div>
          </motion.div>
          <CommitDetails
            isExpanded={isExpanded}
            commitSummary={commit.commit_summary as unknown as string[]}
          />
        </CardContent>
      </Card>
    </motion.div>
  );
}

function CommitDetails({
  isExpanded,
  commitSummary,
}: {
  isExpanded: boolean;
  commitSummary: string[];
}) {
  return (
    <motion.div
      initial={false}
      animate={isExpanded ? 'expanded' : 'collapsed'}
      variants={{
        expanded: { opacity: 1, height: 'auto' },
        collapsed: { opacity: 0, height: 0 },
      }}
      transition={{
        duration: 0.4,
        ease: [0.04, 0.62, 0.23, 0.98],
      }}
    >
      <div className="bg-primary/5 p-6 shadow-[inset_5px_5px_10px_rgba(0,0,0,0.1),inset_-5px_-5px_10px_rgba(255,255,255,0.05)]">
        <motion.h4
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-gray-700 dark:text-gray-200 font-semibold mb-4 flex items-center text-lg"
        >
          <GitCommit className="mr-2 h-5 w-5 text-primary" />
          Commit Details
        </motion.h4>
        <ul className="space-y-3">
          {commitSummary.map((summaryPoint, index) => (
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
              <Code className="w-5 h-5 text-primary mr-3 flex-shrink-0 mt-1" />
              <span className="text-gray-600 dark:text-gray-300">
                {summaryPoint}
              </span>
            </motion.li>
          ))}
        </ul>
      </div>
    </motion.div>
  );
}
