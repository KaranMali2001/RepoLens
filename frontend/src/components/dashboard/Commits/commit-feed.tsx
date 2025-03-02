'use client';

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { useCommits } from '@/hooks/use-commits';
import useProject from '@/hooks/use-project';
import { useState } from 'react';
import { CommitCard } from './commit-card';
import { LoadingSkeleton } from '@/components/loading';

export function CommitFeed() {
  const [expandedCommits, setExpandedCommits] = useState<Set<number>>(
    new Set(),
  );
  const { project } = useProject();
  const {
    data: commits,
    isLoading: isLoadingCommits,
    isError,
  } = useCommits(project?.id);

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

  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>
          An error occurred while fetching commits.
        </AlertDescription>
      </Alert>
    );
  }

  if (isLoadingCommits) {
    return <LoadingSkeleton />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-background/80 p-8">
      <h1 className="text-5xl font-bold text-center mb-12 bg-clip-text text-transparent bg-gradient-to-r from-primary/80 to-primary">
        Commit Chronicle
      </h1>
      <div className="max-w-4xl mx-auto space-y-8">
        {commits?.map((commit, index) => (
          <CommitCard
            key={commit.id}
            commit={commit}
            isExpanded={expandedCommits.has(commit.id!)}
            onToggle={() => toggleCommit(commit.id!)}
            index={index}
          />
        ))}
      </div>
    </div>
  );
}
