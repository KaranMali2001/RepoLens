'use client';
import { fetchProjects } from '@/queries/fetchProjects';
import { ProjectType } from '@/types';
import { useQuery } from '@tanstack/react-query';
import { useLocalStorage } from 'usehooks-ts';

export default function useProject() {
  const {
    data: projects,
    error,
    isLoading,
  } = useQuery<ProjectType[]>({
    queryKey: ['projects', 'persist'],
    queryFn: fetchProjects,
    staleTime: Infinity,
  });
  const [selectedProjectId, setSelectedProjectId] = useLocalStorage(
    'project 1',
    0,
  );
  const project = projects?.find((project) => project.id === selectedProjectId);
  console.log('data from use Project hoojk', projects); //data.data

  return {
    selectedProjectId,
    setSelectedProjectId,
    project,
    projects,
    error,
    isLoading,
  };
}
