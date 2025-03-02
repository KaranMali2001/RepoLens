'use client';
import { fetchProjects } from '@/queries/fetchProjects';
import { ProjectType } from '@/types';
import { useQuery } from '@tanstack/react-query';
import { useLocalStorage } from 'usehooks-ts';

export default function useProject() {
  const {
    data: projectsResponse,
    error,
    isLoading,
  } = useQuery<{ data: ProjectType[] } | ProjectType[]>({
    queryKey: ['projects', 'persist'],
    queryFn: fetchProjects,
    staleTime: Infinity,
  });

  const [selectedProjectId, setSelectedProjectId] = useLocalStorage(
    'project 1',
    0,
  );

  // Handle both nested and non-nested responses
  const projects = Array.isArray(projectsResponse)
    ? projectsResponse
    : projectsResponse?.data;

  let project: ProjectType | undefined;
  if (Array.isArray(projects)) {
    project = projects.find((project) => project.id === selectedProjectId);
  }

  return {
    selectedProjectId,
    setSelectedProjectId,
    project,
    projects,
    error,
    isLoading,
  };
}
