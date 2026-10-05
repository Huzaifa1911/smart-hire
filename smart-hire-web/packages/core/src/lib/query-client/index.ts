import { QueryClient } from '@tanstack/react-query';

/** Shared query-client construction; no queries or mutations are defined. */
export const AppQueryClient = new QueryClient({
  defaultOptions: { queries: { refetchOnWindowFocus: false } },
});
