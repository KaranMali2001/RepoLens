'use client';
import { ClerkProvider } from '@clerk/nextjs';
import { createAsyncStoragePersister } from '@tanstack/query-async-storage-persister';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client';
import localforage from 'localforage';
import { Toaster } from 'sonner';

export function Providers({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: 2,
      },
    },
  });
  const asyncStoragePersister = createAsyncStoragePersister({
    storage: localforage,
  });
  return (
    <PersistQueryClientProvider
      client={queryClient}
      persistOptions={{
        persister: asyncStoragePersister,
        dehydrateOptions: {
          shouldDehydrateQuery: (query) => {
            return query.queryKey.includes('persist');
          },
        },
      }}
    >
      <QueryClientProvider client={queryClient}>
        <Toaster richColors />
        <ClerkProvider>{children}</ClerkProvider>;
      </QueryClientProvider>
    </PersistQueryClientProvider>
  );
}
