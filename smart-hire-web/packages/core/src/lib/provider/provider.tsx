import { useEffect, useMemo, useState, type ReactNode } from 'react';
import { QueryClientProvider } from '@tanstack/react-query';
import { useStore } from 'zustand';

import { APIClient, AuthenticationHandler, authStore } from '@smart-hire/api';

import { AppCoreContext, type IContextState } from '../context/index.js';
import { AppQueryClient } from '../query-client/index.js';

export interface AppCoreProviderProps
  extends Omit<IContextState, 'apiService' | 'accountInfo'> {
  children: ReactNode;
  baseUrl: string;
}

export function AppCoreProvider({
  children,
  baseUrl,
  storageService,
  navigationService,
  alertService,
  contextAwareness,
  featureFlags,
  platformName,
}: AppCoreProviderProps) {
  const [ready, setReady] = useState(false);
  const user = useStore(authStore, (state) => state.user);
  const apiService = useMemo(
    () =>
      new APIClient(
        { iamApiBaseUrl: `${baseUrl.replace(/\/+$/, '')}/iam-service/v1/` },
        {
          contextHeaders: contextAwareness ? { ...contextAwareness } : null,
          useCredentials: false,
        },
      ),
    [baseUrl, contextAwareness],
  );

  const value = useMemo<IContextState>(
    () => ({
      storageService,
      navigationService,
      alertService,
      contextAwareness,
      featureFlags,
      platformName,
      apiService,
      accountInfo: { user },
    }),
    [
      storageService,
      navigationService,
      alertService,
      contextAwareness,
      featureFlags,
      platformName,
      apiService,
      user,
    ],
  );

  useEffect(() => {
    let active = true;

    setReady(false);
    const handler = new AuthenticationHandler({
      iamApiClient: apiService.iamApiClient,
      storageService,
    });

    // init is a no-op scaffold, not a successful authentication attempt.
    void handler.init().finally(() => {
      if (active) setReady(true);
    });

    return () => {
      active = false;
      handler.dispose();
    };
  }, [apiService, storageService]);

  if (!ready) return null;

  return (
    <AppCoreContext.Provider value={value}>
      <QueryClientProvider client={AppQueryClient}>
        {children}
      </QueryClientProvider>
    </AppCoreContext.Provider>
  );
}
