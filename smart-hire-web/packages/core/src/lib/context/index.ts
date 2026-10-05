import { createContext, useContext } from 'react';

import type {
  AccountInfo,
  StorageService,
  NavigationService,
  AlertService,
} from '@smart-hire/types';
import type { APIClient } from '@smart-hire/api';

export interface ContextAwareness {
  experience?: string;
  application?: string;
}

export interface IContextState {
  accountInfo: AccountInfo;
  contextAwareness: ContextAwareness | null;
  featureFlags?: Record<string, boolean>;
  storageService: StorageService;
  navigationService: NavigationService;
  alertService: AlertService;
  apiService: APIClient;
  platformName: string;
}

export const AppCoreContext = createContext<IContextState | null>(null);

export function useAppCoreContext(): IContextState {
  const context = useContext(AppCoreContext);

  if (!context) throw new Error('useAppCoreContext requires AppCoreProvider');

  return context;
}
