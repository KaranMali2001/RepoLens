import { GetCommits } from '@/queries/getCommits';
import { CommitType } from '@/types';
import { useQuery } from '@tanstack/react-query';
import { AxiosError } from 'axios';

export function useCommits(project_id: number | undefined) {
  return useQuery<CommitType[], AxiosError>({
    queryKey: ['commits', project_id],
    queryFn: () => GetCommits(project_id),
    retry: false,
    staleTime: 5 * 60 * 1000,
    gcTime: 30 * 60 * 1000,
    enabled: !!project_id,
  });
}
